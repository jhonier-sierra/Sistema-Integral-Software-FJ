
# =====================================================
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ARCHIVO: servicios.py
# DESCRIPCION: Gestion de servicios especializados
# =====================================================

# Importacion de herramientas para clases abstractas
from abc import ABC, abstractmethod

# Importacion de excepciones personalizadas
from excepciones import (
    DatosInvalidosError,
    CalculoInconsistenteError,
    ServicioNoDisponibleError
)

import math


# =====================================================
# CLASE ABSTRACTA SERVICIO
# =====================================================

class Servicio(ABC):

    def __init__(self, identificador, nombre, precio_base):

        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError(
                "El identificador del servicio es obligatorio."
            )

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError(
                "El nombre del servicio es obligatorio."
            )

        self.__identificador = identificador.strip()
        self.__nombre = nombre.strip()

        self.__precio_base = self._validar_numero(
            precio_base, "El precio base"
        )

        if self.__precio_base <= 0:
            raise DatosInvalidosError(
                "El precio base debe ser mayor que cero."
            )

        self.__disponible = True

    # Validar valores numericos
    @staticmethod
    def _validar_numero(valor, descripcion):

        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise DatosInvalidosError(
                f"{descripcion} debe ser un numero."
            )

        if not math.isfinite(valor):
            raise DatosInvalidosError(
                f"{descripcion} debe ser un numero finito."
            )

        return float(valor)

    # Consultar identificador
    @property
    def identificador(self):
        return self.__identificador

    # Consultar nombre
    @property
    def nombre(self):
        return self.__nombre

    # Consultar precio base
    @property
    def precio_base(self):
        return self.__precio_base

    # Consultar disponibilidad
    @property
    def disponible(self):
        return self.__disponible

    # Cambiar disponibilidad
    def cambiar_disponibilidad(self, estado):

        if not isinstance(estado, bool):
            raise DatosInvalidosError(
                "La disponibilidad debe ser verdadera o falsa."
            )

        self.__disponible = estado

    # Calcular costo con impuestos y descuentos opcionales
    def _aplicar_cargos(self, costo, impuesto=0, descuento=0):

        impuesto = self._validar_numero(
            impuesto, "El impuesto"
        )

        descuento = self._validar_numero(
            descuento, "El descuento"
        )

        if not 0 <= impuesto <= 100:
            raise DatosInvalidosError(
                "El impuesto debe estar entre 0 y 100."
            )

        if not 0 <= descuento <= 100:
            raise DatosInvalidosError(
                "El descuento debe estar entre 0 y 100."
            )

        resultado = costo * (1 - descuento / 100)
        resultado = resultado * (1 + impuesto / 100)

        if not math.isfinite(resultado) or resultado < 0:
            raise CalculoInconsistenteError(
                "El resultado del calculo no es valido."
            )

        return round(resultado, 2)

    # Metodo abstracto para calcular costos
    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        pass

    # Metodo abstracto para describir servicios
    @abstractmethod
    def describir_servicio(self):
        pass

    # Metodo abstracto para validar parametros
    @abstractmethod
    def validar_parametros(self):
        pass


# =====================================================
# SERVICIO 1: RESERVA DE SALAS
# =====================================================

class ReservaSala(Servicio):

    def __init__(self, identificador, nombre, precio_base, capacidad):

        super().__init__(identificador, nombre, precio_base)

        if isinstance(capacidad, bool) or not isinstance(capacidad, int):
            raise DatosInvalidosError(
                "La capacidad debe ser un numero entero."
            )

        if capacidad <= 0:
            raise DatosInvalidosError(
                "La capacidad debe ser mayor que cero."
            )

        self.__capacidad = capacidad

    @property
    def capacidad(self):
        return self.__capacidad

    # Validar parametros de la sala
    def validar_parametros(self):

        if self.__capacidad <= 0:
            raise DatosInvalidosError(
                "La capacidad de la sala no es valida."
            )

        return True

    # Calcular costo de reserva por horas
    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        if not self.disponible:
            raise ServicioNoDisponibleError(
                "La sala no se encuentra disponible."
            )

        self.validar_parametros()

        duracion = self._validar_numero(
            duracion, "La duracion"
        )

        if duracion <= 0:
            raise DatosInvalidosError(
                "La duracion debe ser mayor que cero."
            )

        costo = self.precio_base * duracion

        return self._aplicar_cargos(costo, impuesto, descuento)

    # Describir servicio
    def describir_servicio(self):

        return (
            f"Reserva de sala: {self.nombre}\n"
            f"Capacidad: {self.__capacidad} personas\n"
            f"Precio por hora: ${self.precio_base:,.2f}"
        )


# =====================================================
# SERVICIO 2: ALQUILER DE EQUIPOS
# =====================================================

class AlquilerEquipo(Servicio):

    def __init__(self, identificador, nombre, precio_base, cantidad):

        super().__init__(identificador, nombre, precio_base)

        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise DatosInvalidosError(
                "La cantidad de equipos debe ser un entero."
            )

        if cantidad <= 0:
            raise DatosInvalidosError(
                "La cantidad de equipos debe ser mayor que cero."
            )

        self.__cantidad = cantidad

    @property
    def cantidad(self):
        return self.__cantidad

    # Validar parametros del equipo
    def validar_parametros(self):

        if self.__cantidad <= 0:
            raise DatosInvalidosError(
                "La cantidad de equipos no es valida."
            )

        return True

    # Calcular costo por horas y cantidad de equipos
    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        if not self.disponible:
            raise ServicioNoDisponibleError(
                "El equipo no se encuentra disponible."
            )

        self.validar_parametros()

        duracion = self._validar_numero(
            duracion, "La duracion"
        )

        if duracion <= 0:
            raise DatosInvalidosError(
                "La duracion debe ser mayor que cero."
            )

        costo = self.precio_base * duracion * self.__cantidad

        return self._aplicar_cargos(costo, impuesto, descuento)

    # Describir servicio
    def describir_servicio(self):

        return (
            f"Alquiler de equipo: {self.nombre}\n"
            f"Cantidad de equipos: {self.__cantidad}\n"
            f"Precio por hora y equipo: ${self.precio_base:,.2f}"
        )


# =====================================================
# SERVICIO 3: ASESORIAS ESPECIALIZADAS
# =====================================================

class Asesoria(Servicio):

    def __init__(self, identificador, nombre, precio_base, especialidad):

        super().__init__(identificador, nombre, precio_base)

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidosError(
                "La especialidad de la asesoria es obligatoria."
            )

        self.__especialidad = especialidad.strip()

    @property
    def especialidad(self):
        return self.__especialidad

    # Validar parametros de la asesoria
    def validar_parametros(self):

        if not self.__especialidad:
            raise DatosInvalidosError(
                "La especialidad no puede estar vacia."
            )

        return True

    # Calcular costo de asesoria por horas
    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        if not self.disponible:
            raise ServicioNoDisponibleError(
                "La asesoria no se encuentra disponible."
            )

        self.validar_parametros()

        duracion = self._validar_numero(
            duracion, "La duracion"
        )

        if duracion <= 0:
            raise DatosInvalidosError(
                "La duracion debe ser mayor que cero."
            )

        costo = self.precio_base * duracion

        return self._aplicar_cargos(costo, impuesto, descuento)

    # Describir servicio
    def describir_servicio(self):

        return (
            f"Asesoria especializada: {self.nombre}\n"
            f"Especialidad: {self.__especialidad}\n"
            f"Precio por hora: ${self.precio_base:,.2f}"
        )


# =====================================================
# FIN DEL ARCHIVO SERVICIOS
# =====================================================
