
# =====================================================
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ARCHIVO: gestor.py
# DESCRIPCION: Administracion general del sistema
# =====================================================

from clientes import Cliente
from servicios import Servicio
from reservas import Reserva

from excepciones import (
    DatosInvalidosError,
    ClienteNoEncontradoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError
)

from registro import registrar_evento, registrar_error


class SistemaGestion:

    def __init__(self):
        # Listas internas del sistema
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

    # ================================================
    # GESTION DE CLIENTES
    # ================================================

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El objeto no es un cliente valido.")

        for existente in self.__clientes:
            if existente.identificador == cliente.identificador:
                raise DatosInvalidosError(
                    "Ya existe un cliente con ese documento."
                )

        self.__clientes.append(cliente)
        registrar_evento(
            f"Cliente registrado: {cliente.identificador}"
        )
        return "Cliente registrado correctamente."

    def buscar_cliente(self, documento):
        for cliente in self.__clientes:
            if cliente.identificador == documento:
                return cliente

        raise ClienteNoEncontradoError(
            f"No se encontro el cliente {documento}."
        )

    # ================================================
    # GESTION DE SERVICIOS
    # ================================================

    def registrar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El objeto no es un servicio valido.")

        for existente in self.__servicios:
            if existente.identificador == servicio.identificador:
                raise DatosInvalidosError(
                    "Ya existe un servicio con ese identificador."
                )

        self.__servicios.append(servicio)
        registrar_evento(
            f"Servicio registrado: {servicio.identificador}"
        )
        return "Servicio registrado correctamente."

    def buscar_servicio(self, identificador):
        for servicio in self.__servicios:
            if servicio.identificador == identificador:
                return servicio

        raise ServicioNoDisponibleError(
            f"No se encontro el servicio {identificador}."
        )

    # ================================================
    # GESTION DE RESERVAS
    # ================================================

    def crear_reserva(self, identificador, documento,
                      id_servicio, duracion,
                      impuesto=0, descuento=0):

        cliente = self.buscar_cliente(documento)
        servicio = self.buscar_servicio(id_servicio)

        for existente in self.__reservas:
            if existente.identificador == identificador:
                raise ReservaInvalidaError(
                    "Ya existe una reserva con ese identificador."
                )

        reserva = Reserva(
            identificador,
            cliente,
            servicio,
            duracion,
            impuesto,
            descuento
        )

        self.__reservas.append(reserva)

        registrar_evento(
            f"Reserva creada: {identificador}"
        )

        return reserva

    def buscar_reserva(self, identificador):
        for reserva in self.__reservas:
            if reserva.identificador == identificador:
                return reserva

        raise ReservaInvalidaError(
            f"No se encontro la reserva {identificador}."
        )

    def confirmar_reserva(self, identificador):
        reserva = self.buscar_reserva(identificador)
        resultado = reserva.confirmar()

        registrar_evento(
            f"Reserva confirmada: {identificador}"
        )

        return resultado

    def cancelar_reserva(self, identificador):
        reserva = self.buscar_reserva(identificador)
        resultado = reserva.cancelar()

        registrar_evento(
            f"Reserva cancelada: {identificador}"
        )

        return resultado

    def procesar_reserva(self, identificador):
        reserva = self.buscar_reserva(identificador)

        try:
            resultado = reserva.procesar()
            registrar_evento(
                f"Reserva procesada: {identificador}"
            )
            return resultado

        except Exception as error:
            registrar_error(
                f"Error al procesar la reserva {identificador}",
                error
            )
            raise

    # ================================================
    # CONSULTAS GENERALES
    # ================================================

    def listar_clientes(self):
        return [
            cliente.obtener_informacion()
            for cliente in self.__clientes
        ]

    def listar_servicios(self):
        return [
            servicio.describir_servicio()
            for servicio in self.__servicios
        ]

    def listar_reservas(self):
        return [
            reserva.obtener_informacion()
            for reserva in self.__reservas
        ]
