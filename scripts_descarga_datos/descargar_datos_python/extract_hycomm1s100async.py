from dataclasses import dataclass
from pickletools import float8
import httpx
import aiofiles
import asyncio
from pathlib import Path
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta
import logging
from tqdm import tqdm
from enum import Enum
import sys

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Configurar Clase Enum
class DownloadStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"


@dataclass(frozen=True)
class DownloadSettings:
    chunk_size: int = 512 * 1024
    connect: float = 180.0
    read: float = 300.0
    write: float = 300.0
    pool: float = 300.0
    max_keepalive_connections: int = 3
    max_connections: int = 8
    max_concurrent: int = 5


async def downloader(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    data_url: httpx.URL,
    output_file: Path,
    download_settings: DownloadSettings,
) -> DownloadStatus:
    """
    Descarga un archivo NetCDF grande usando streaming
    con barra de progreso
    """
    filename: str = output_file.name

    try:
        # Hacer request con streaming
        async with semaphore:
            async with client.stream("GET", data_url) as response:
                response.raise_for_status()

                # Obtener tamaño total si está disponible
                total_size: int = int(response.headers.get("content-length", 0))

                # Descargar con barra de progreso
                async with aiofiles.open(output_file, "wb") as f:
                    downloaded = 0
                    async for chunk in response.aiter_bytes(
                        chunk_size=download_settings.chunk_size
                    ):
                        if chunk:
                            await f.write(chunk)
                            downloaded += len(chunk)

                logger.info(
                    f"Download complete: {output_file}. Final size: {downloaded / (1024 * 1024):.2f} MB"
                )

                return DownloadStatus.SUCCESS

    except httpx.RequestError as e:
        logger.error(f"Request error for {filename}: {e}")
        return DownloadStatus.FAILED
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error {e.response.status_code} for {filename}: {e}")
        return DownloadStatus.FAILED
    except Exception as e:
        logger.error(f"Unexpected error downloading {filename}: {e}")
        return DownloadStatus.FAILED


async def download_data(
    download_settings: DownloadSettings,
    url_list: list[str],
    output_file_list: list[Path],
):
    # Configuración del cliente
    timeout: httpx.Timeout = httpx.Timeout(
        connect=download_settings.connect,
        read=download_settings.read,
        write=download_settings.write,
        pool=download_settings.pool,
    )
    limits: httpx.Limits = httpx.Limits(
        max_keepalive_connections=download_settings.max_keepalive_connections,
        max_connections=download_settings.max_connections,
    )
    # Creacion del semaforo
    semaphore: asyncio.Semaphore = asyncio.Semaphore(download_settings.max_concurrent)

    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        tasks = [
            asyncio.create_task(
                downloader(client, semaphore, url, output_file, download_settings)
            )
            for url, output_file in zip(url_list, output_file_list)
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)


def parse_date_range(start_date: str, end_date: str) -> tuple[datetime, datetime]:
    try:
        data_start_date: datetime = datetime.strptime(start_date, "%Y-%j-%H")
        data_end_date: datetime = datetime.strptime(end_date, "%Y-%j-%H")

        if data_start_date > data_end_date:
            raise ValueError("Start date must be before end date")

        return data_start_date, data_end_date
    except ValueError as e:
        logger.error(f"Date parsing error: {e}")
        raise


def create_file_info(current_date: datetime) -> tuple[str, Path]:
    # Extraer componentes de fecha
    year: int = current_date.year
    day: str = current_date.strftime("%j")
    hour: int = current_date.hour

    # Crear nombre de archivo y rutas
    filename: str = f"010_archv.{year}_{day}_{hour:02d}_2d.nc"
    output_directory: Path = Path(f"datos_hycomm_1_100/{year}")
    output_directory.mkdir(parents=True, exist_ok=True)
    output_file: Path = output_directory / filename

    return filename, output_file


def create_download_url(filename: str, year: int) -> httpx.URL:
    # Crear URL
    url: str = f"https://tds.hycom.org/thredds/fileServer/datasets/GOMb0.01/reanalysis/data/{year}/{filename}"
    return httpx.URL(url)


def download_with_retries(
    data_url: httpx.URL,
    output_file: Path,
    download_settings: DownloadSettings,
) -> DownloadStatus:
    # Intentar descargar el archivo con reintentos limitados
    status: DownloadStatus = DownloadStatus.FAILED
    retry: int = 0
    while status == DownloadStatus.FAILED and retry <= download_settings.retries_number:
        status = descargar_datos_hycomm(data_url, output_file, download_settings)
        if status == DownloadStatus.FAILED:
            retry += 1
            if retry <= download_settings.retries_number:
                logger.warning(
                    f"Retry {retry}/{download_settings.retries_number} in {download_settings.sleep_time} seconds..."
                )
                time.sleep(download_settings.sleep_time)
            else:
                logger.error(
                    f"Download failed after {download_settings.retries_number} retries: {output_file.name}"
                )

    return status


def main() -> None:
    start_date: str = "2001-355-10"
    end_date: str = "2001-355-14"

    try:
        data_start_date, data_end_date = parse_date_range(start_date, end_date)
    except ValueError:
        sys.exit(1)

    download_settings: DownloadSettings = DownloadSettings()

    current_date = data_start_date  # Variable de control del ciclo while
    processed_files: int = 0  # Contador de archivos procesados
    downloaded_files: int = 0  # Contador de archivos descargados
    failed_files: int = 0  # Contador de archivos no descargados
    existing_files: int = 0  # Contador de archivos existentes
    url_list = []
    output_file_list = []

    while current_date <= data_end_date:
        processed_files += 1

        filename, output_file = create_file_info(current_date)

        # Verifica si el archivo ya existe
        if output_file.exists():
            logger.info(f"File exists: {filename}, skipping downloaded...")
            existing_files += 1
            current_date += relativedelta(hours=1)  # Avanzar a la siguiente hora
            continue

        # Crear URL
        data_url = create_download_url(filename, current_date.year)

        url_list.append(data_url)
        output_file_list.append(output_file)

        # Avanzar a la siguiente hora
        current_date += relativedelta(hours=1)

    asyncio.run(download_data(download_settings, url_list, output_file_list))
    # Intentar descargar el archivo con reintentos limitados
    # status = download_with_retries(data_url, output_file, download_settings)

    # Contador de archivos descargados exitosamente
    # if status == DownloadStatus.SUCCESS:
    #     downloaded_files += 1
    # else:
    #     failed_files += 1

    # Resumen final
    logger.info("=" * 50)
    logger.info("Download Summary")
    logger.info(f"Processed files: {processed_files}")
    logger.info(f"Downloaded files: {downloaded_files}")
    logger.info(f"Existing files: {existing_files}")
    logger.info(f"Failed files: {failed_files}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
