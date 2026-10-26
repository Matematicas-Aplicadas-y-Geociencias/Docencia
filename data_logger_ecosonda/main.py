import logging
import argparse
from leerDatosSonda import SondaDatos, SondaConfig
from datetime import datetime

def leer_argumentos():
    parser = argparse.ArgumentParser(
        description="Registra los datos NMEA de la Sonda en un archivo."
    )

    parser.add_argument(
        "--puerto-com",
        default=SondaConfig.puerto_com,
        help="Puerto serial, p. ej. COM5 (default: %(default)s)",
    )

    parser.add_argument(
        "--baudrate",
        type=int,
        default=SondaConfig.baudrate,
        help="Baudios (default: %(default)s)",
    )
    return parser.parse_args()

def main():
    args = leer_argumentos()
    # Configurar logging con formato estándar de timestamp, nivel y mensaje
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)

    parametros = SondaConfig(puerto_com=args.puerto_com, baudrate=args.baudrate)
    sensor = SondaDatos(parametros)
    nombre_archivo = datetime.now().strftime("sonda_data_%d%m%Y.txt")
    try:
        with open(nombre_archivo, "a", encoding="utf-8") as archivo:
            logger.info(f"Guardando en {nombre_archivo}...")
            while True:
                linea = sensor.read_line()
                if linea:
                    logger.info(repr(linea))
                    archivo.write(linea + "\n")
                    archivo.flush()
    except KeyboardInterrupt:
        pass
    finally:
        sensor.close()


if __name__ == "__main__":
    main()
