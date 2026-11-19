
# =====================================================
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ARCHIVO: clientes.py
# DESCRIPCION: Gestion y validacion de clientes
# =====================================================

# Importacion de la clase abstracta Entidad
from entidades import Entidad

# Importacion de excepciones personalizadas
from excepciones import DatosInvalidosError

# Importacion de expresiones regulares
import re


# Clase Cliente que hereda de Entidad
class Cliente(Entidad):

    # Constructor de la clase Cliente
    def __init__(self, documento, nombre, correo, telefono):

        # Inicializar la clase padre
        super().__init__(documento)

        # Validar los datos del cliente
        self.__validar_nombre(nombre)
        self.__validar_correo(correo)
        self.__validar_telefono(telefono)

        # Atributos privados del cliente
        self.__nombre = nombre.strip()
        self.__correo = correo.strip().lower()
        self.__telefono = telefono.strip()

    # Validar el nombre del cliente
    def __validar_nombre(self, nombre):

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError(
                "El nombre del cliente no puede estar vacio."
            )

        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+", nombre.strip()):
            raise DatosInvalidosError(
                "El nombre contiene caracteres no permitidos."
            )

    # Validar el correo electronico
    def __validar_correo(self, correo):

        if not isinstance(correo, str) or not correo.strip():
            raise DatosInvalidosError(
                "El correo electronico es obligatorio."
            )

        patron = r"^[\w.+-]+@[\w-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(patron, correo.strip()):
            raise DatosInvalidosError(
                "El correo electronico no tiene un formato valido."
            )

    # Validar el telefono
    def __validar_telefono(self, telefono):

        if not isinstance(telefono, str) or not telefono.strip():
            raise DatosInvalidosError(
                "El telefono es obligatorio."
            )

        if not telefono.isdigit() or not 7 <= len(telefono) <= 15:
            raise DatosInvalidosError(
                "El telefono debe contener entre 7 y 15 digitos."
            )

    # Consultar el nombre del cliente
    @property
    def nombre(self):
        return self.__nombre

    # Consultar el correo del cliente
    @property
    def correo(self):
        return self.__correo

    # Consultar el telefono del cliente
    @property
    def telefono(self):
        return self.__telefono

    # Obtener toda la informacion del cliente
    def obtener_informacion(self):

        return (
            f"Documento: {self.identificador}\n"
            f"Nombre: {self.__nombre}\n"
            f"Correo: {self.__correo}\n"
            f"Telefono: {self.__telefono}"
        )


# =====================================================
# FIN DEL ARCHIVO CLIENTES
# =====================================================
