import httpx
import asyncio
import aiofiles
from pathlib import Path
import time
import logging
from typing import Optional, Callable

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def download_file(session: httpx.AsyncClient,
                       url: str,
                       filename: str,
                       semaphore: asyncio.Semaphore,
                       chunk_size: int = 1024*1024,
                       progress_callback: Optional[Callable] = None) -> dict:
    """
    Descarga un archivo individual de forma asíncrona

    Args:
        session: Cliente httpx
        url: URL del archivo
        filename: Ruta local donde guardar
        semaphore: Semáforo para controlar concurrencia
        chunk_size: Tamaño del chunk en bytes
        progress_callback: Función opcional para progreso
    """
    async with semaphore:
        start_time = time.time()
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        try:
            logger.info(f"Iniciando descarga: {filename}")

            async with session.stream("GET", url) as response:
                response.raise_for_status()

                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0

                async with aiofiles.open(filepath, 'wb') as file:
                    async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                        await file.write(chunk)
                        downloaded += len(chunk)

                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(filename, progress, downloaded, total_size)

            elapsed_time = time.time() - start_time
            speed_mbps = (downloaded / (1024*1024)) / elapsed_time if elapsed_time > 0 else 0

            logger.info(f"Completado: {filename} ({downloaded/(1024*1024):.1f} MB en {elapsed_time:.1f}s - {speed_mbps:.1f} MB/s)")

            return {
                'filename': filename,
                'status': 'success',
                'size_bytes': downloaded,
                'time_seconds': elapsed_time,
                'speed_mbps': speed_mbps
            }

        except Exception as e:
            logger.error(f"Error descargando {filename}: {str(e)}")
            return {
                'filename': filename,
                'status': 'error',
                'error': str(e)
            }

def simple_progress_callback(filename: str, progress: float, downloaded: int, total: int):
    """Callback simple para mostrar progreso"""
    if progress % 10 < 1:  # Mostrar cada 10%
        print(f"{Path(filename).name}: {progress:.1f}% ({downloaded/(1024*1024):.1f}/{total/(1024*1024):.1f} MB)")

async def download_multiple_files(url: str,
                                filename: str,
                                max_concurrent: int = 5,
                                chunk_size: int = 1024*1024,
                                progress_callback: Optional[Callable] = None):
    """
    Descarga múltiples archivos de forma asíncrona

    Args:
        urls_and_filenames: Lista de tuplas (url, filename)
        max_concurrent: Número máximo de descargas simultáneas
        chunk_size: Tamaño del chunk en bytes
        progress_callback: Función callback para progreso

    Returns:
        Lista de diccionarios con resultados
    """
    # Configuración del cliente
    timeout = httpx.Timeout(connect=30.0, read=300.0, write=300.0, pool=300.0)
    limits = httpx.Limits(max_keepalive_connections=3, max_connections=8)
    semaphore = asyncio.Semaphore(max_concurrent)

    async with httpx.AsyncClient(timeout=timeout, limits=limits) as session:
        task = download_file(
                session, url, filename, semaphore, chunk_size,
                progress_callback or simple_progress_callback
            )

        results = await asyncio.gather(task, return_exceptions=True)
        return results

if __name__ == "__main__":
    url_data = "https://tds.hycom.org/thredds/fileServer/datasets/GOMb0.01/reanalysis/data/2001/010_archv.2001_016_00_2d.nc"
    print("=== Ejemplo 1: Función completa ===")
    results = asyncio.run(download_multiple_files(url_data, "output/010_archv.2001_016_00_2d.nc", max_concurrent=2))
