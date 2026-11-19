
# =====================================================
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ARCHIVO: reservas.py
# DESCRIPCION: Gestion, confirmacion y cancelacion
# de reservas de clientes y servicios
# =====================================================

# Importacion de la clase Cliente
from clientes import Cliente

# Importacion de la clase abstracta Servicio
from servicios import Servicio

# Importacion de excepciones personalizadas
from excepciones import (
    DatosInvalidosError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError
)

import math


# =====================================================
# CLASE RESERVA
# =====================================================

class Reserva:

    # Constructor de la clase
    def __init__(
        self,
        identificador,
        cliente,
        servicio,
        duracion,
        impuesto=0,
        descuento=0
    ):

        # Validar identificador
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError(
                "El identificador de la reserva es obligatorio."
            )

        # Validar que el cliente sea un objeto Cliente
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError(
                "La reserva requiere un cliente valido."
            )

        # Validar que el servicio sea un objeto Servicio
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError(
                "La reserva requiere un servicio valido."
            )

        # Validar duracion
        self.__validar_numero(duracion, "La duracion")

        if duracion <= 0:
            raise DatosInvalidosError(
                "La duracion debe ser mayor que cero."
            )

        # Validar impuesto y descuento
        self.__validar_porcentaje(impuesto, "El impuesto")
        self.__validar_porcentaje(descuento, "El descuento")

        # Atributos encapsulados
        self.__identificador = identificador.strip()
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = float(duracion)
        self.__impuesto = float(impuesto)
        self.__descuento = float(descuento)

        # Estado inicial de la reserva
        self.__estado = "Pendiente"

        # Costo inicial sin calcular
        self.__costo_total = None

    # =================================================
    # METODOS DE VALIDACION
    # =================================================

    @staticmethod
    def __validar_numero(valor, descripcion):

        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise DatosInvalidosError(
                f"{descripcion} debe ser un numero."
            )

        if not math.isfinite(valor):
            raise DatosInvalidosError(
                f"{descripcion} debe ser un numero finito."
            )

    @staticmethod
    def __validar_porcentaje(valor, descripcion):

        Reserva.__validar_numero(valor, descripcion)

        if not 0 <= valor <= 100:
            raise DatosInvalidosError(
                f"{descripcion} debe estar entre 0 y 100."
            )

    # =================================================
    # PROPIEDADES PARA CONSULTAR INFORMACION
    # =================================================

    @property
    def identificador(self):
        return self.__identificador

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    # =================================================
    # CONFIRMAR RESERVA
    # =================================================

    def confirmar(self):

        if self.__estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        if not self.__servicio.disponible:
            raise ServicioNoDisponibleError(
                "No es posible confirmar la reserva: "
                "el servicio no esta disponible."
            )

        # Calcular el costo del servicio
        self.__costo_total = self.__servicio.calcular_costo(
            self.__duracion,
            self.__impuesto,
            self.__descuento
        )

        # Actualizar el estado
        self.__estado = "Confirmada"

        return (
            f"Reserva {self.__identificador} confirmada correctamente."
        )

    # =================================================
    # CANCELAR RESERVA
    # =================================================

    def cancelar(self):

        if self.__estado == "Cancelada":
            raise OperacionNoPermitidaError(
                "La reserva ya se encuentra cancelada."
            )

        if self.__estado == "Procesada":
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva procesada."
            )

        self.__estado = "Cancelada"

        return (
            f"Reserva {self.__identificador} cancelada correctamente."
        )

    # =================================================
    # PROCESAR RESERVA
    # =================================================

    def procesar(self):

        try:

            # Confirmar automaticamente si esta pendiente
            if self.__estado == "Pendiente":
                self.confirmar()

            # Verificar que se encuentre confirmada
            if self.__estado != "Confirmada":
                raise OperacionNoPermitidaError(
                    "La reserva debe estar confirmada para procesarse."
                )

            # Verificar que exista un costo calculado
            if self.__costo_total is None:
                raise ReservaInvalidaError(
                    "La reserva no tiene un costo calculado."
                )

            # Cambiar estado de la reserva
            self.__estado = "Procesada"

            return (
                f"Reserva {self.__identificador} procesada correctamente.\n"
                f"Cliente: {self.__cliente.nombre}\n"
                f"Servicio: {self.__servicio.nombre}\n"
                f"Costo total: ${self.__costo_total:,.2f}"
            )

        except Exception as error:

            # Encadenamiento de excepciones
            raise ReservaInvalidaError(
                f"No fue posible procesar la reserva "
                f"{self.__identificador}."
            ) from error

    # =================================================
    # OBTENER INFORMACION DE LA RESERVA
    # =================================================

    def obtener_informacion(self):

        costo = (
            f"${self.__costo_total:,.2f}"
            if self.__costo_total is not None
            else "Pendiente de calculo"
        )

        return (
            f"Identificador: {self.__identificador}\n"
            f"Cliente: {self.__cliente.nombre}\n"
            f"Servicio: {self.__servicio.nombre}\n"
            f"Duracion: {self.__duracion} horas\n"
            f"Estado: {self.__estado}\n"
            f"Costo: {costo}"
        )


# =====================================================
# FIN DEL ARCHIVO RESERVAS
# =====================================================
