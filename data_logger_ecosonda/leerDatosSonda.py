import time
import logging
import serial
from dataclasses import dataclass

# Configurar logging con formato estándar de timestamp, nivel y mensaje
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SondaConfig:
    puerto_com: str = "COM5"
    baudrate: int = 4800
    timeout: float = 1.0
    reintento_s: float = 3.0


class SondaDatos:
    def __init__(self, parametros: SondaConfig):
        self.parametros = parametros
        self.ser = None
        self._connect()

    def _connect(self):
        """Establece conexión persistente con la Sonda"""
        self.close()
        try:
            self.ser = serial.Serial(
                self.parametros.puerto_com,
                self.parametros.baudrate,
                timeout=self.parametros.timeout,
            )
            self.ser.reset_input_buffer()  # Descarta bytes viejos o incompletos
            logger.info(
                f"Conectado a la Sonda en {self.parametros.puerto_com} @ {self.parametros.baudrate}"
            )
        except serial.SerialException as e:
            logger.error(
                f"No se ha podido conectar a la Sonda en el puerto {self.parametros.puerto_com}: {e}"
            )
            self.ser = None

    def read_line(self):
        """Devuelve una línea de texto, o None si no hubo dato o no hay conexión."""
        if self.ser is None or not self.ser.is_open:
            self._connect()
        if self.ser is None:
            logger.warning(
                f"Reintentando conectar con la Sonda en {self.parametros.reintento_s} s..."
            )
            time.sleep(self.parametros.reintento_s)
            return None

        try:
            linea = self.ser.readline().decode("ascii", errors="replace").strip()
        except serial.SerialException as e:
            logger.error(f"Se perdio la conexion : {e}")
            self.close()
            return None

        return linea or None  # cadena vacía (timeout) -> None

    def close(self):
        """Cierra la conexión serial"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            logger.info("Conexión serial cerrada")
        self.ser = None
