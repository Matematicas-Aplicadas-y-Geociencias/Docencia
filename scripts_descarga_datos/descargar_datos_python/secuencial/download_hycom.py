import logging
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

import httpx
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

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
    sleep_time: int = 8
    timeout: float = 300.0
    retries_number: int = 10


def descargar_datos_hycomm(
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
        with httpx.Client(timeout=download_settings.timeout) as client:
            # Hacer request con streaming
            with client.stream("GET", data_url) as response:
                response.raise_for_status()

                # Obtener tamaño total si está disponible
                total_size: int = int(response.headers.get("content-length", 0))

                # Descargar con barra de progreso
                with open(output_file, "wb") as f:
                    with tqdm(
                        total=total_size,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                        desc=f"Downloading {filename}",
                    ) as pbar:
                        downloaded = 0
                        for chunk in response.iter_bytes(
                            chunk_size=download_settings.chunk_size
                        ):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                pbar.update(len(chunk))

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


def parse_date_range(start_date: str, end_date: str) -> tuple[datetime, datetime]:
    try:
        data_start_date: datetime = datetime.strptime(start_date, "%Y-%j")
        data_end_date: datetime = datetime.strptime(end_date, "%Y-%j")

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

    # Crear nombre de archivo y rutas
    filename: str = f"gomb4_daily_{year}_{day}_2d.nc"
    output_directory: Path = Path(f"datos_hycomm_1_25/{year}")
    output_directory.mkdir(parents=True, exist_ok=True)
    output_file: Path = output_directory / filename

    return filename, output_file


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


def create_download_url(filename: str, year: int) -> httpx.URL:
    # Crear URL
    # https://data.hycom.org/datasets/GOMe0.04/expt_03.9/data/daily_netcdf/2024/gomb4_daily_2024_246_2d.nc
    url: str = f"https://data.hycom.org/datasets/GOMe0.04/expt_03.9/data/daily_netcdf/{year}/{filename}"
    return httpx.URL(url)


def main() -> None:
    start_date: str = "2024-248"
    end_date: str = "2024-263"

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

    while current_date <= data_end_date:
        processed_files += 1

        filename, output_file = create_file_info(current_date)

        # Verifica si el archivo ya existe
        if output_file.exists():
            logger.info(f"File exists: {filename}, skipping downloaded...")
            existing_files += 1
            current_date += relativedelta(days=1)  # Avanzar a la siguiente hora
            continue

        # Crear URL
        data_url = create_download_url(filename, current_date.year)

        # Intentar descargar el archivo con reintentos limitados
        status = download_with_retries(data_url, output_file, download_settings)

        # Contador de archivos descargados exitosamente
        if status == DownloadStatus.SUCCESS:
            downloaded_files += 1
        else:
            failed_files += 1

        # Avanzar a la siguiente hora
        current_date += relativedelta(days=1)

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
