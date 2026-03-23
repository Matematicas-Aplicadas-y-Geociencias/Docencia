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

# Configurar logging con formato estándar de timestamp, nivel y mensaje
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DownloadStatus(Enum):
    """Estado del resultado de una descarga."""

    SUCCESS = "success"
    FAILED = "failed"


@dataclass(frozen=True)
class DownloadSettings:
    """Configuración inmutable para el proceso de descarga.

    Attributes:
        chunk_size: Tamaño de cada fragmento de descarga en bytes.
        sleep_time: Segundos de espera entre reintentos.
        timeout: Tiempo máximo de espera por respuesta del servidor en segundos.
        retries_number: Número máximo de reintentos ante fallos.
    """

    chunk_size: int = 512 * 1024
    sleep_time: int = 8
    timeout: float = 300.0
    retries_number: int = 10


def stream_to_file(
    response: httpx.Response, output_file: Path, total_size: int, chunk_size: int
) -> int:
    """Escribe el contenido de una respuesta HTTP en disco usando streaming.

    Muestra una barra de progreso durante la escritura.

    Args:
        response: Respuesta HTTP activa con streaming habilitado.
        output_file: Ruta del archivo de destino.
        total_size: Tamaño total esperado en bytes (0 si no está disponible).
        chunk_size: Tamaño de cada fragmento leído en bytes.

    Returns:
        Total de bytes escritos a disco.
    """

    downloaded: int = 0
    filename: str = output_file.name
    with open(output_file, "wb") as f:
        with tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=f"Downloading {filename}",
        ) as pbar:
            for chunk in response.iter_bytes(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    pbar.update(len(chunk))

    return downloaded


def request_data(
    client: httpx.Client,
    data_url: httpx.URL,
    output_file: Path,
    download_settings: DownloadSettings,
) -> DownloadStatus:
    """Realiza la petición HTTP y delega la escritura del archivo.

    Usa streaming para manejar archivos grandes sin cargarlos en memoria.

    Args:
        client: Cliente HTTP configurado con timeout.
        data_url: URL del archivo a descargar.
        output_file: Ruta donde se guardará el archivo.
        download_settings: Configuración de la descarga.

    Returns:
        DownloadStatus.SUCCESS si la descarga completó correctamente.

    Raises:
        httpx.HTTPStatusError: Si el servidor responde con un código de error.
    """

    chunk_size: int = download_settings.chunk_size

    with client.stream("GET", data_url) as response:
        response.raise_for_status()

        # Obtener tamaño total si el servidor lo proporciona
        total_size: int = int(response.headers.get("content-length", 0))

        downloaded: int = stream_to_file(response, output_file, total_size, chunk_size)

        logger.info(
            f"Download complete: {output_file}. Final size: {downloaded / (1024 * 1024):.2f} MB"
        )

        return DownloadStatus.SUCCESS


def download_data(
    data_url: httpx.URL,
    output_file: Path,
    download_settings: DownloadSettings,
) -> DownloadStatus:
    """Descarga un archivo con reintentos ante fallos recuperables.

    Reintenta ante errores de red y códigos HTTP 429/5xx. No reintenta
    ante errores irrecuperables como 404 o 403.

    Args:
        data_url: URL del archivo a descargar.
        output_file: Ruta donde se guardará el archivo.
        download_settings: Configuración con número de reintentos y tiempos de espera.

    Returns:
        DownloadStatus.SUCCESS si la descarga fue exitosa,
        DownloadStatus.FAILED si se agotaron los reintentos.
    """

    filename: str = output_file.name
    status: DownloadStatus = DownloadStatus.FAILED
    retry: int = 0
    while status == DownloadStatus.FAILED and retry <= download_settings.retries_number:
        try:
            with httpx.Client(timeout=download_settings.timeout) as client:
                status = request_data(client, data_url, output_file, download_settings)
        except httpx.RequestError as e:
            # Errores de red (timeout, conexión rechazada, DNS) — siempre reintentables
            logger.error(f"Request error for {filename}: {e}")
            status = DownloadStatus.FAILED
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            if status_code in {429, 500, 502, 503, 504}:
                # Errores temporales del servidor — vale la pena reintentar
                logger.warning(f"HTTP error {status_code} for {filename}, will retry")
                status = DownloadStatus.FAILED  # reintenta
            else:
                # Errores permanentes (404, 403, 401) — reintentar no tiene sentido
                logger.error(f"HTTP error {status_code} for {filename}: {e}")
                return DownloadStatus.FAILED
        except Exception as e:
            # Red de seguridad para errores inesperados
            logger.error(f"Unexpected error downloading {filename}: {e}")
            status = DownloadStatus.FAILED

        if status == DownloadStatus.FAILED:
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

    return status


def parse_and_validate_date_range(
    start_date: str, end_date: str
) -> tuple[datetime, datetime]:
    """Parsea y valida un rango de fechas en formato HYCOM.

    El formato esperado es %Y-%j-%H (año-día_juliano-hora).

    Args:
        start_date: Fecha de inicio como string, e.g. "2001-365-18".
        end_date: Fecha de fin como string, e.g. "2002-001-11".

    Returns:
        Tupla (start, end) como objetos datetime.

    Raises:
        ValueError: Si el formato es inválido o start_date > end_date.
    """

    try:
        data_start_date: datetime = datetime.strptime(start_date, "%Y-%j")
        data_end_date: datetime = datetime.strptime(end_date, "%Y-%j")

        if data_start_date > data_end_date:
            raise ValueError("Start date must be before end date")

        return data_start_date, data_end_date
    except ValueError as e:
        logger.error(f"Date parsing error: {e}")
        raise


def create_file_info(current_date: datetime) -> Path:
    """Construye la ruta de salida para un archivo NetCDF dado una fecha.

    El nombre sigue la convención HYCOM: gomb4_daily_{año}_{día}_2d.nc
    El directorio de salida se organiza por año bajo datos_hycomm_1_25/.

    Args:
        current_date: Fecha y hora del archivo a construir.

    Returns:
        Ruta completa del archivo de salida (sin crearlo en disco).
    """

    year: int = current_date.year
    day: str = current_date.strftime("%j")

    filename: str = f"gomb4_daily_{year}_{day}_2d.nc"
    output_directory: Path = Path(f"datos_hycomm_1_25/{year}")
    output_file: Path = output_directory / filename

    return output_file


def create_download_url(filename: str, year: int) -> httpx.URL:
    """Construye la URL de descarga HYCOM para un archivo dado.

    Args:
        filename: Nombre del archivo NetCDF a descargar.
        year: Año del archivo, usado para construir la ruta en el servidor.

    Returns:
        URL completa del archivo en el servidor DATA de HYCOM.
    """

    # https://data.hycom.org/datasets/GOMe0.04/expt_03.9/data/daily_netcdf/2024/gomb4_daily_2024_246_2d.nc
    url: str = f"https://data.hycom.org/datasets/GOMe0.04/expt_03.9/data/daily_netcdf/{year}/{filename}"
    return httpx.URL(url)


def main() -> None:
    """Punto de entrada principal del script de descarga HYCOM.

    Itera hora a hora entre start_date y end_date, descargando los archivos
    NetCDF correspondientes. Omite archivos que ya existen en disco y
    registra un resumen al finalizar.
    """

    start_date: str = "2024-248"
    end_date: str = "2024-253"

    try:
        data_start_date, data_end_date = parse_and_validate_date_range(
            start_date, end_date
        )
    except ValueError:
        sys.exit(1)

    download_settings: DownloadSettings = DownloadSettings()

    current_date = data_start_date  # Variable de control del ciclo while
    processed_files: int = 0  # Contador de archivos procesados
    downloaded_files: int = 0  # Contador de archivos descargados exitosamente
    failed_files: int = 0  # Contador de archivos con fallo en descarga
    existing_files: int = 0  # Contador de archivos ya existentes en disco

    while current_date <= data_end_date:
        processed_files += 1

        output_file = create_file_info(current_date)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        filename = output_file.name

        # Omitir archivos que ya fueron descargados en ejecuciones anteriores
        if output_file.exists():
            logger.info(f"File exists: {filename}, skipping download...")
            existing_files += 1
            current_date += relativedelta(days=1)  # Avanzar al siguiente dia
            continue

        data_url = create_download_url(filename, current_date.year)

        status = download_data(data_url, output_file, download_settings)

        if status == DownloadStatus.SUCCESS:
            downloaded_files += 1
        else:
            failed_files += 1

        current_date += relativedelta(days=1)

    # Resumen final del proceso de descarga
    logger.info("=" * 50)
    logger.info("Download Summary")
    logger.info(f"Processed files: {processed_files}")
    logger.info(f"Downloaded files: {downloaded_files}")
    logger.info(f"Existing files: {existing_files}")
    logger.info(f"Failed files: {failed_files}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
