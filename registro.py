
# =====================================================
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ARCHIVO: registro.py
# DESCRIPCION: Registro de eventos y errores
# =====================================================

from datetime import datetime
import os

# Ruta del archivo de registro
CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_LOG = os.path.join(CARPETA, "logs.txt")


def registrar_evento(mensaje):
    """Registra una operacion realizada correctamente."""
    escribir_registro("EVENTO", mensaje)


def registrar_error(mensaje, error=None):
    """Registra un error ocurrido durante la ejecucion."""
    detalle = mensaje

    if error is not None:
        detalle += (
            f" | Tipo: {type(error).__name__}"
            f" | Detalle: {error}"
        )

    escribir_registro("ERROR", detalle)


def escribir_registro(tipo, mensaje):
    """Escribe la informacion en el archivo logs.txt."""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(f"[{fecha}] [{tipo}] {mensaje}\n")

    except OSError as error:
        print("Advertencia: no fue posible escribir en el archivo de registro.")
        print(f"Detalle: {error}")
