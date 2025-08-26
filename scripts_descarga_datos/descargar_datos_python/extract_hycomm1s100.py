import httpx
from pathlib import Path
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta
import logging
from tqdm import tqdm
from enum import Enum

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurar Enum
class Descarga(Enum):
    EXITOSA = True
    FALLIDA = False
    ARCHIVO_EXISTE = "existe"

class Constante(Enum):
    TAMNIO_CHUNK_DEFAULT = 32*1024
    TIEMPO_ESPERA = 8
    REINTENTOS_MAXIMOS = 10
    TIMEOUT = 300.0

def descargar_datos_hycomm(
    url_datos: httpx.URL,
    ruta_descarga_datos: Path,
    chunk_size=Constante.TAMNIO_CHUNK_DEFAULT.value) -> Descarga:
    """
    Descarga un archivo NetCDF grande usando streaming
    con barra de progreso
    """
    # Verifica si el archivo ya existe
    nombre_archivo = ruta_descarga_datos.name
    if ruta_descarga_datos.exists():
        logger.info(f"Archivo ya existe: {nombre_archivo}, no se descargará de nuevo...")
        return Descarga.ARCHIVO_EXISTE

    try:
        with httpx.Client(timeout=Constante.TIMEOUT.value) as client:
            # Hacer request con streaming
            with client.stream('GET', url_datos) as response:
                response.raise_for_status()

                # Obtener tamaño total si está disponible
                total_size = int(response.headers.get('content-length', 0))

                # Descargar con barra de progreso
                with open(ruta_descarga_datos, 'wb') as f:
                    with tqdm(
                        total=total_size,
                        unit='B',
                        unit_scale=True,
                        unit_divisor=1024,
                        desc=f"Descargando {nombre_archivo}"
                    ) as pbar:
                        downloaded = 0
                        for chunk in response.iter_bytes(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                pbar.update(len(chunk))

                logger.info(f"Descarga completada: {ruta_descarga_datos}. Tamaño final: {downloaded / (1024*1024):.2f} MB")

                return Descarga.EXITOSA

    except httpx.RequestError as e:
        logger.error(f"Error de conexión: {e}")
        return Descarga.FALLIDA
    except httpx.HTTPStatusError as e:
        logger.error(f"Error HTTP {e.response.status_code}: {e}")
        return Descarga.FALLIDA
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return Descarga.FALLIDA

def main():
    fecha_inicial: str = '2001-365-21'
    fecha_final: str = '2002-001-09'

    try:
        fecha_datos_inicial: datetime = datetime.strptime(fecha_inicial, '%Y-%j-%H')
        fecha_datos_final: datetime = datetime.strptime(fecha_final, '%Y-%j-%H')
    except ValueError as e:
        logger.error(f"Error al convertir fechas: {e}")
        return

    fecha = fecha_datos_inicial     # Variable de control del ciclo while
    archivos_procesados: int = 0    # Contador de archivos procesados
    archivos_descargados: int = 0   # Contador de archivos descargados
    archivos_fallidos: int = 0      # Contador de archivos no descargados

    while fecha <= fecha_datos_final:
        archivos_procesados += 1

        # Extraer componentes de fecha
        anio: int = fecha.year
        dia: str = fecha.strftime('%j')
        hora: int = fecha.hour

        # Crear nombre de archivo y rutas
        nombre_archivo: str = f'010_archv.{anio}_{dia}_{hora:02d}_2d.nc'
        directorio_descargas_datos: Path = Path(f'datos_hycomm_1_100/{anio}')
        directorio_descargas_datos.mkdir(parents=True, exist_ok=True)
        ruta_descarga_datos: Path = directorio_descargas_datos / nombre_archivo

        # Crear URL
        url: str = f'https://tds.hycom.org/thredds/fileServer/datasets/GOMb0.01/reanalysis/data/{anio}/{nombre_archivo}'
        url_datos: httpx.URL = httpx.URL(url)
        logger.info(f"Procesando: {ruta_descarga_datos}")

        # Intentar descarga con reintentos limitados
        estatus = Descarga.FALLIDA
        reintentos = 0
        while estatus == Descarga.FALLIDA and reintentos <= Constante.REINTENTOS_MAXIMOS.value:
            estatus = descargar_datos_hycomm(url_datos, ruta_descarga_datos)
            if estatus == Descarga.FALLIDA:
                reintentos += 1
                if reintentos <= Constante.REINTENTOS_MAXIMOS.value:
                    logger.warning(f"Reintento {reintentos}/{Constante.REINTENTOS_MAXIMOS.value} en {Constante.TIEMPO_ESPERA.value} segundos...")
                    time.sleep(Constante.TIEMPO_ESPERA.value)
                else:
                    logger.error(f"Falló después de {Constante.REINTENTOS_MAXIMOS.value} reintentos: {nombre_archivo}")
                    archivos_fallidos += 1

        # Contador de archivos descargados exitosamente
        if estatus == Descarga.EXITOSA:
            archivos_descargados += 1

        # Avanzar a la siguiente hora
        fecha += relativedelta(hours=1)

    # Resumen final
    logger.info("="*50)
    logger.info("RESUMEN DE DESCARGA")
    logger.info(f"Archivos procesados: {archivos_procesados}")
    logger.info(f"Archivos descargados: {archivos_descargados}")
    logger.info(f"Archivos que ya existían: {archivos_procesados - archivos_descargados - archivos_fallidos}")
    logger.info(f"Archivos fallidos: {archivos_fallidos}")
    logger.info("="*50)

if __name__ == "__main__":
    main()
