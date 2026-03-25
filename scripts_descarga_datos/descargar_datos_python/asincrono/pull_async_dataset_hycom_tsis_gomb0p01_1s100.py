"""
HYCOM-TSIS 1/100° Gulf of Mexico Reanalysis

    Title: HYCOM-TSIS GOMb0.01
    Resolution: 1/100% (~1km)
    Domain: Extends from 98°E to 77°E in longitude and from 18°N to 32°N in latitude
    Date/Data Range: 2001-01-16 to 2024-04-28
    HYCOM version: 2.3.01

    Experiment numbers:

        YYYY: year, DDD: day, HH: hour, NN: Netcdf type (i.e. 2d or 3z)
        HYCOM-TSIS GOMb0.01:

        010_archv.YYYY_DDD_HH_NN.nc: 2001_016_00 to 2017_152_18
        023_archv.YYYY_DDD_HH_NN.nc: 2017_152_19 to 2024_001_18
        026_archv.YYYY_DDD_HH_NN.nc: 2024_001_19 to 2024_119_23
        027_archv.YYYY_DDD_HH_NN.nc: 2024_092_19 to 2024_245_18 (Date range: 2024-04-01 to 2024-09-01)

    URL de los datos:
        https://www.hycom.org/data/gomb0pt01/gom-reanalysis
        https://tds.hycom.org/thredds/catalog/datasets/GOMb0.01/reanalysis/data/catalog.html
"""

import asyncio
import logging
import sys
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

import aiofiles
import httpx
from dateutil.relativedelta import relativedelta

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
class ConnectionSettings:
    """Configuración inmutable para el cliente HTTP.

    Attributes:
        connect: Tiempo máximo en segundos para establecer la conexión.
        read: Tiempo máximo en segundos para leer la respuesta.
        write: Tiempo máximo en segundos para enviar la petición.
        pool: Tiempo máximo en segundos para obtener una conexión del pool.
        max_keepalive_connections: Número máximo de conexiones persistentes en el pool.
        max_connections: Número máximo total de conexiones simultáneas.
    """

    connect: float = 180.0
    read: float = 300.0
    write: float = 300.0
    pool: float = 300.0
    max_keepalive_connections: int = 3
    max_connections: int = 8


@dataclass(frozen=True)
class DownloadSettings:
    """Configuración inmutable para el proceso de descarga.

    Attributes:
        chunk_size: Tamaño de cada fragmento de descarga en bytes.
        max_concurrent: Número máximo de descargas concurrentes.
    """

    chunk_size: int = 512 * 1024
    max_concurrent: int = 5


async def stream_to_file(
    response: httpx.Response,
    output_file: Path,
    chunk_size: int,
) -> int:
    """Escribe el contenido de una respuesta HTTP en disco usando streaming.

    Args:
        response: Respuesta HTTP activa con streaming habilitado.
        output_file: Ruta del archivo de destino.
        chunk_size: Tamaño de cada fragmento leído en bytes.

    Returns:
        Total de bytes escritos a disco.
    """
    downloaded: int = 0

    async with aiofiles.open(output_file, "wb") as f:
        async for chunk in response.aiter_bytes(chunk_size=chunk_size):
            if chunk:
                await f.write(chunk)
                downloaded += len(chunk)

        return downloaded


async def request_data(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    data_url: httpx.URL,
    output_file: Path,
    download_settings: DownloadSettings,
) -> DownloadStatus:
    """Realiza la petición HTTP y delega la escritura del archivo.

    Usa streaming para manejar archivos grandes sin cargarlos en memoria.
    El semáforo limita el número de descargas simultáneas.

    Args:
        client: Cliente HTTP asíncrono compartido entre tareas.
        semaphore: Semáforo para controlar la concurrencia de descargas.
        data_url: URL del archivo a descargar.
        output_file: Ruta donde se guardará el archivo.
        download_settings: Configuración de la descarga.

    Returns:
        DownloadStatus.SUCCESS si la descarga completó correctamente,
        DownloadStatus.FAILED en caso de error.
    """

    filename: str = output_file.name

    try:
        # Hacer request con streaming
        async with semaphore:
            async with client.stream("GET", data_url) as response:
                response.raise_for_status()

                # Obtener tamaño total si está disponible
                # total_size: int = int(response.headers.get("content-length", 0))
                downloaded = await stream_to_file(
                    response, output_file, download_settings.chunk_size
                )

        logger.info(
            f"Download complete: {output_file}. Final size: {downloaded / (1024 * 1024):.2f} MB"
        )

        return DownloadStatus.SUCCESS

    except httpx.RequestError as e:
        # Errores de red: timeout, conexión rechazada, DNS
        logger.error(f"Request error for {filename}: {e}")
        return DownloadStatus.FAILED
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error {e.response.status_code} for {filename}: {e}")
        return DownloadStatus.FAILED
    except Exception as e:
        # Red de seguridad para errores inesperados
        logger.error(f"Unexpected error downloading {filename}: {e}")
        return DownloadStatus.FAILED


async def download_data(
    url_list: list[httpx.URL],
    output_file_list: list[Path],
    download_settings: DownloadSettings,
    connection_settings: ConnectionSettings,
) -> list[DownloadStatus | BaseException]:
    """Descarga múltiples archivos de forma concurrente.

    Construye el cliente HTTP, el semáforo y lanza todas las tareas
    en paralelo usando asyncio.gather.

    Args:
        url_list: Lista de URLs a descargar.
        output_file_list: Lista de rutas de destino, en el mismo orden que url_list.
        download_settings: Configuración de descarga (chunk size, concurrencia).
        connection_settings: Configuración del cliente HTTP (timeouts, pool).

    Returns:
        Lista de resultados en el mismo orden que url_list. Cada elemento es
        DownloadStatus.SUCCESS, DownloadStatus.FAILED, o una excepción si
        return_exceptions=True la capturó.
    """

    timeout: httpx.Timeout = httpx.Timeout(
        connect=connection_settings.connect,
        read=connection_settings.read,
        write=connection_settings.write,
        pool=connection_settings.pool,
    )
    limits: httpx.Limits = httpx.Limits(
        max_keepalive_connections=connection_settings.max_keepalive_connections,
        max_connections=connection_settings.max_connections,
    )
    # Limita el número de descargas simultáneas independientemente del pool HTTP
    semaphore: asyncio.Semaphore = asyncio.Semaphore(download_settings.max_concurrent)

    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        tasks = [
            asyncio.create_task(
                request_data(client, semaphore, url, output_file, download_settings)
            )
            for url, output_file in zip(url_list, output_file_list)
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)


def create_filename_info(base_directory: Path, current_date: datetime) -> Path:
    """Construye la ruta de salida para un archivo NetCDF dado una fecha.

    El nombre sigue la convención HYCOM: 010_archv.{año}_{día}_{hora}_2d.nc
    El directorio de salida se organiza por año bajo base_directory.

    Args:
        base_directory: Directorio raíz donde se guardan los archivos.
        current_date: Fecha y hora del archivo a construir.

    Returns:
        Ruta completa del archivo de salida (sin crearlo en disco).
    """

    year: int = current_date.year
    day: str = current_date.strftime("%j")
    hour: int = current_date.hour

    # Nombre de archivo siguiendo la convención HYCOM
    filename: str = f"010_archv.{year}_{day}_{hour:02d}_2d.nc"
    output_directory: Path = base_directory / f"{year}"
    output_file: Path = output_directory / filename

    return output_file


def create_download_url(filename: str, year: int) -> httpx.URL:
    """Construye la URL de descarga HYCOM para un archivo dado.

    Args:
        filename: Nombre del archivo NetCDF a descargar.
        year: Año del archivo, usado para construir la ruta en el servidor.

    Returns:
        URL completa del archivo en el servidor THREDDS de HYCOM.
    """

    url: str = f"https://tds.hycom.org/thredds/fileServer/datasets/GOMb0.01/reanalysis/data/{year}/{filename}"
    return httpx.URL(url)


def parse_and_validate_date_range(
    start_date: str, end_date: str, date_format: str
) -> tuple[datetime, datetime]:
    """Parsea y valida un rango de fechas en formato HYCOM.

    El formato esperado es %Y-%j-%H (año-día_juliano-hora).

    Args:
        start_date: Fecha de inicio como string, e.g. "2001-365-18".
        end_date: Fecha de fin como string, e.g. "2002-001-11".
        date_format: Formato strptime para parsear las fechas.

    Returns:
        Tupla (start, end) como objetos datetime.

    Raises:
        ValueError: Si el formato es inválido o start_date > end_date.
    """

    try:
        data_start_date: datetime = datetime.strptime(start_date, date_format)
        data_end_date: datetime = datetime.strptime(end_date, date_format)

        if data_start_date > data_end_date:
            raise ValueError("Start date must be before end date")

        return data_start_date, data_end_date
    except ValueError as e:
        logger.error(f"Date parsing error: {e}")
        raise


def main() -> None:
    """Punto de entrada principal del script de descarga HYCOM.

    Itera hora a hora entre start_date y end_date, construye las listas
    de URLs y rutas de salida omitiendo archivos ya existentes, y lanza
    todas las descargas de forma concurrente. Registra un resumen al finalizar.

    """

    start_date_string: str = "2002-365-08"
    end_date_string: str = "2003-001-21"
    date_format: str = "%Y-%j-%H"
    base_directory: Path = Path("datos_hycomm_1_100")

    try:
        start_date, end_date = parse_and_validate_date_range(
            start_date_string, end_date_string, date_format
        )
    except ValueError:
        sys.exit(1)

    download_settings: DownloadSettings = DownloadSettings()
    connection_settings: ConnectionSettings = ConnectionSettings()

    current_date: datetime = start_date  # Variable de control del ciclo while
    processed_files: int = 0  # Contador de archivos procesados
    downloaded_files: int = 0  # Contador de archivos descargados exitosamente
    failed_files: int = 0  # Contador de archivos con fallo en descarga
    existing_files: int = 0  # Contador de archivos ya existentes en disco
    url_list: list[httpx.URL] = []
    output_file_list: list[Path] = []

    while current_date <= end_date:
        processed_files += 1

        output_file = create_filename_info(base_directory, current_date)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        filename = output_file.name

        # Omitir archivos ya descargados en ejecuciones anteriores
        if output_file.exists():
            logger.info(f"File exists: {filename}, skipping download...")
            existing_files += 1
            current_date += relativedelta(hours=1)  # Avanzar a la siguiente hora
            continue

        data_url = create_download_url(filename, current_date.year)

        url_list.append(data_url)
        output_file_list.append(output_file)

        current_date += relativedelta(hours=1)

    status = asyncio.run(
        download_data(
            url_list, output_file_list, download_settings, connection_settings
        )
    )

    # Contabilizar resultados de cada tarea
    for result in status:
        if result == DownloadStatus.SUCCESS:
            downloaded_files += 1
        else:
            failed_files += 1

    # Resumen final del proceso
    logger.info("=" * 50)
    logger.info("Download Summary")
    logger.info(f"Processed files: {processed_files}")
    logger.info(f"Downloaded files: {downloaded_files}")
    logger.info(f"Existing files: {existing_files}")
    logger.info(f"Failed files: {failed_files}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
