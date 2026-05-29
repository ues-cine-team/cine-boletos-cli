"""
CineLogger
Módulo de logging centralizado para el sistema de venta de boletos.

¿Por qué existe?
----------------
Registra eventos importantes del sistema como:
- compras realizadas,
- errores ocurridos,
- asientos bloqueados o liberados,
- operaciones rechazadas.

Esto permite hacer seguimiento de lo que pasa en el sistema
y detectar problemas fácilmente.
"""

import logging
import os
from datetime import datetime


def get_logger(name: str = "cine_boletos") -> logging.Logger:
    """
    Retorna un logger configurado para el sistema.

    Parameters
    ----------
    name : str
        Nombre del logger. Por defecto 'cine_boletos'.

    Returns
    -------
    logging.Logger
        Logger listo para usar.
    """
    logger = logging.getLogger(name)

    # Evitar agregar handlers duplicados si ya fue configurado
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Formato de los mensajes
    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s - %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler para mostrar en consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para guardar en archivo
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "cine_boletos.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Logger global del sistema listo para importar
logger = get_logger("cine_boletos")


"""
Ejemplo de uso
--------------
from infrastructure.logging.logger import logger

logger.info("Compra realizada: boleto #123")
logger.warning("Asiento A1 bloqueado por más de 5 minutos")
logger.error("Error al procesar pago: timeout")
logger.debug("Lock registrado para showtime-1, seat A3")
"""
