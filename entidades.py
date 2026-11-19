
# =====================================================
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ARCHIVO: entidades.py
# DESCRIPCION: Clase abstracta general del sistema
# =====================================================

# Importacion de herramientas para crear clases abstractas
from abc import ABC, abstractmethod


# Clase abstracta que representa las entidades del sistema
class Entidad(ABC):

    # Constructor de la clase
    def __init__(self, identificador):

        # Validar que el identificador no este vacio
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("El identificador no puede estar vacio.")

        # Atributo encapsulado de la entidad
        self.__identificador = identificador.strip()

    # Metodo getter para consultar el identificador
    @property
    def identificador(self):
        return self.__identificador

    # Metodo abstracto para obtener informacion
    @abstractmethod
    def obtener_informacion(self):
        """Metodo que deben implementar las clases derivadas."""
        pass


# =====================================================
# FIN DEL ARCHIVO ENTIDADES
# =====================================================
