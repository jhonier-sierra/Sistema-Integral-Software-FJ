
# =====================================================
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ARCHIVO: excepciones.py
# DESCRIPCION: Excepciones personalizadas del sistema
# =====================================================


# Clase base para los errores del sistema
class SoftwareFJError(Exception):
    """Clase base de las excepciones de Software FJ."""

    pass


# Error cuando los datos ingresados son incorrectos
class DatosInvalidosError(SoftwareFJError):
    """Se produce cuando un dato no cumple las validaciones."""

    pass


# Error cuando un cliente no existe
class ClienteNoEncontradoError(SoftwareFJError):
    """Se produce cuando no se encuentra un cliente."""

    pass


# Error cuando un servicio no está disponible
class ServicioNoDisponibleError(SoftwareFJError):
    """Se produce cuando un servicio no puede utilizarse."""

    pass


# Error cuando una reserva presenta inconsistencias
class ReservaInvalidaError(SoftwareFJError):
    """Se produce cuando una reserva no cumple las condiciones."""

    pass


# Error cuando se intenta realizar una operación no permitida
class OperacionNoPermitidaError(SoftwareFJError):
    """Se produce cuando una operación no está autorizada."""

    pass


# Error cuando falta un parámetro obligatorio
class ParametroFaltanteError(SoftwareFJError):
    """Se produce cuando no se proporciona un parámetro necesario."""

    pass


# Error cuando un cálculo presenta resultados inconsistentes
class CalculoInconsistenteError(SoftwareFJError):
    """Se produce cuando un cálculo no genera un resultado válido."""

    pass


# =====================================================
# FIN DEL ARCHIVO DE EXCEPCIONES PERSONALIZADAS
# =====================================================
