import httpx
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
from tqdm import tqdm

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def descargar_datos_hycomm(url_datos: httpx.URL, ruta_descarga_datos: Path, chunk_size=1024*32):
    """
    Descarga un archivo NetCDF grande usando streaming
    con barra de progreso
    """
    try:
        with httpx.Client(timeout=300.0) as client:
            # Hacer request con streaming
            with client.stream('GET', url_datos) as response:
                response.raise_for_status()

                # Obtener tamaño total si está disponible
                total_size = int(response.headers.get('content-length', 0))

                nombre_archivo = ruta_descarga_datos.name

                # Descargar con barra de progreso
                with open(ruta_descarga_datos, 'wb') as f:
                    with tqdm(
                        total=total_size,
                        unit='B',
                        unit_scale=True,
                        desc=f"Descargando {nombre_archivo}"
                    ) as pbar:
                        downloaded = 0
                        for chunk in response.iter_bytes(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                pbar.update(len(chunk))

                print(f"\n✅ Descarga completada: {ruta_descarga_datos}")
                print(f"📁 Tamaño final: {downloaded / (1024*1024):.2f} MB")

                return True

    except httpx.RequestError as e:
        print(f"❌ Error de conexión: {e}")
        return False
    except httpx.HTTPStatusError as e:
        print(f"❌ Error HTTP {e.response.status_code}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    fecha_inicial: str = '2001-365-22'
    fecha_final: str = '2002-004-13'
    fecha_datos_inicial: datetime = datetime.strptime(fecha_inicial, '%Y-%j-%H')
    fecha_datos_final: datetime = datetime.strptime(fecha_final, '%Y-%j-%H')

    fecha = fecha_datos_inicial

    while fecha <= fecha_datos_final:
        #
        anio: int = fecha.year
        dia: str = fecha.strftime('%j')
        hora: int = fecha.hour
        #
        nombre_archivo: str = f'010_archv.{anio}_{dia}_{hora:02d}_2d.nc'
        directorio_descargas_datos: Path = Path(f'datos_hycomm_1_100/{anio}')
        directorio_descargas_datos.mkdir(parents=True, exist_ok=True)
        ruta_descarga_datos: Path = directorio_descargas_datos / nombre_archivo
        print(ruta_descarga_datos)
        #
        url: str = f'https://tds.hycom.org/thredds/fileServer/datasets/GOMb0.01/reanalysis/data/{anio}/{nombre_archivo}'
        url_datos: httpx.URL = httpx.URL(url)
        descargar_datos_hycomm(url_datos, ruta_descarga_datos)
        #
        fecha += relativedelta(hours=1)


if __name__ == "__main__":
    # fecha_inicial: str = '2001-016-00'
    # fecha_datos: datetime = datetime.strptime(fecha_inicial, '%Y-%j-%H') + relativedelta(hours=4)
    # anio: int = fecha_datos.year
    # dia: str = fecha_datos.strftime('%j')
    # hora: int = fecha_datos.hour
    # #
    # nombre_archivo: str = f'010_archv.{anio}_{dia}_{hora:02d}_2d.nc'
    # directorio_descargas_datos: Path = Path(f'datos_hycomm_1_100/{anio}')
    # directorio_descargas_datos.mkdir(parents=True, exist_ok=True)
    # ruta_descarga_datos: Path = directorio_descargas_datos / nombre_archivo
    # #
    # url: str = f'https://tds.hycom.org/thredds/fileServer/datasets/GOMb0.01/reanalysis/data/{anio}/{nombre_archivo}'
    # url_datos: httpx.URL = httpx.URL(url)
    # #
    # print(ruta_descarga_datos)
    # print(url_datos)
    # descargar_datos_hycomm(url_datos, ruta_descarga_datos)
    main()
