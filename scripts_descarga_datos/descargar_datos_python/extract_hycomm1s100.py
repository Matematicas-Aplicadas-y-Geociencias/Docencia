from dataclasses import dataclass
import httpx
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
    SUCESS = True
    FAIL = False


@dataclass(frozen=True)
class DownloadSettings:
    chunk_size: int
    sleep_time: int
    timeout: float
    retries_number: int


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
                        for chunk in response.iter_bytes(chunk_size=download_settings.chunk_size):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                pbar.update(len(chunk))

                logger.info(
                    f"Download complete: {output_file}. Final size: {downloaded / (1024 * 1024):.2f} MB"
                )

                return DownloadStatus.SUCESS

    except httpx.RequestError as e:
        logger.error(f"{type(e).__name__}: {e}")
        return DownloadStatus.FAIL
    except httpx.HTTPStatusError as e:
        logger.error(f"{type(e).__name__} {e.response.status_code}: {e}")
        return DownloadStatus.FAIL
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        return DownloadStatus.FAIL


def main() -> None:
    start_date: str = "2001-365-20"
    end_date: str = "2002-001-08"

    try:
        data_start_date: datetime = datetime.strptime(start_date, "%Y-%j-%H")
        data_end_date: datetime = datetime.strptime(end_date, "%Y-%j-%H")
    except ValueError as e:
        logger.error(f"{type(e).__name__}: {e}.")
        sys.exit(1)

    download_settings: DownloadSettings = DownloadSettings(
        chunk_size = 512 * 1024,
        sleep_time = 8,
        timeout = 300.0,
        retries_number = 10
    )

    current_date = data_start_date # Variable de control del ciclo while
    processed_files: int = 0  # Contador de archivos procesados
    downloaded_files: int = 0  # Contador de archivos descargados
    failed_files: int = 0  # Contador de archivos no descargados

    while current_date <= data_end_date:
        processed_files += 1

        # Extraer componentes de fecha
        year: int = current_date.year
        day: str = current_date.strftime("%j")
        hour: int = current_date.hour

        # Crear nombre de archivo y rutas
        filename: str = f"010_archv.{year}_{day}_{hour:02d}_2d.nc"
        output_directory: Path = Path(f"datos_hycomm_1_100/{year}")
        output_directory.mkdir(parents=True, exist_ok=True)
        output_file: Path = output_directory / filename

        # Crear URL
        url: str = f"https://tds.hycom.org/thredds/fileServer/datasets/GOMb0.01/reanalysis/data/{year}/{filename}"
        data_url: httpx.URL = httpx.URL(url)

        # Verifica si el archivo ya existe
        if output_file.exists():
            logger.info(
                f"File exists: {filename}, skipping downloaded..."
            )
            current_date += relativedelta(hours=1)  # Avanzar a la siguiente hora
            continue

        # Intentar descargar el archivo con reintentos limitados
        status: DownloadStatus = DownloadStatus.FAIL
        retry: int = 0
        while status == DownloadStatus.FAIL and retry <= download_settings.retries_number:
            status = descargar_datos_hycomm(data_url, output_file, download_settings)
            if status == DownloadStatus.FAIL:
                retry += 1
                if retry <= download_settings.retries_number:
                    logger.warning(
                        f"Retry {retry}/{download_settings.retries_number} in {download_settings.sleep_time} seconds..."
                    )
                    time.sleep(download_settings.sleep_time)
                else:
                    logger.error(
                        f"Download failed after {download_settings.retries_number} retries: {filename}"
                    )
                    failed_files += 1

        # Contador de archivos descargados exitosamente
        if status == DownloadStatus.SUCESS:
            downloaded_files += 1

        # Avanzar a la siguiente hora
        current_date += relativedelta(hours=1)

    # Resumen final
    logger.info("=" * 50)
    logger.info("Download Summary")
    logger.info(f"Processed files: {processed_files}")
    logger.info(f"Downloaded files: {downloaded_files}")
    logger.info(
        f"Existing files: {processed_files - downloaded_files - failed_files}"
    )
    logger.info(f"Failed files: {failed_files}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
