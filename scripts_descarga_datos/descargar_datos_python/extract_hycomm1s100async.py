from dataclasses import dataclass
import httpx
import aiofiles
import asyncio
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
from enum import Enum

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
    url_list: list[httpx.URL],
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


def get_filename(date: datetime) -> str:
    # Extraer componentes de fecha
    year: int = date.year
    day: str = date.strftime("%j")
    hour: int = date.hour

    # Crear nombre de archivo
    filename: str = f"010_archv.{year}_{day}_{hour:02d}_2d.nc"

    return filename


def create_output_directory(base_directory: Path, date: datetime) -> Path:
    # Extraer componentes de fecha
    year: str = str(date.year)

    # rutas
    output_directory: Path = base_directory / year
    output_directory.mkdir(parents=True, exist_ok=True)

    return output_directory


def create_download_url(filename: str, date: datetime) -> httpx.URL:
    # Crear URL
    year: int = date.year
    url: str = f"https://tds.hycom.org/thredds/fileServer/datasets/GOMb0.01/reanalysis/data/{year}/{filename}"
    return httpx.URL(url)


def main() -> None:
    start_date_string: str = "2002-365-22"
    end_date_string: str = "2003-002-05"
    format: str = "%Y-%j-%H"
    base_directory: Path = Path("datos_hycomm_1_100")

    start_date: datetime = datetime.strptime(start_date_string, format)
    end_date: datetime = datetime.strptime(end_date_string, format)

    if start_date > end_date:
        raise ValueError("Start date must be before end date")

    download_settings: DownloadSettings = DownloadSettings()

    current_date: datetime = start_date  # Variable de control del ciclo while
    processed_files: int = 0  # Contador de archivos procesados
    downloaded_files: int = 0  # Contador de archivos descargados
    failed_files: int = 0  # Contador de archivos no descargados
    existing_files: int = 0  # Contador de archivos existentes
    url_list: list[httpx.URL] = []
    output_file_list: list[Path] = []

    while current_date <= end_date:
        processed_files += 1

        filename = get_filename(current_date)
        output_directory = create_output_directory(base_directory, current_date)
        output_file: Path = output_directory / filename

        # Verifica si el archivo ya existe
        if output_file.exists():
            logger.info(f"File exists: {filename}, skipping downloaded...")
            existing_files += 1
            current_date += relativedelta(hours=1)  # Avanzar a la siguiente hora
            continue

        # Crear URL
        data_url = create_download_url(filename, current_date)

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
