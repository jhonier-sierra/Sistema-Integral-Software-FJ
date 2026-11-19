
# =====================================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: main.py
# SISTEMA INTEGRAL DE GESTION
# =====================================================

from gestor import SistemaGestion
from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from registro import registrar_evento, registrar_error

from excepciones import (
    DatosInvalidosError,
    ClienteNoEncontradoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError
)


def ejecutar_prueba(numero, descripcion, operacion):
    print("\n" + "=" * 55)
    print(f"OPERACION {numero}: {descripcion}")
    print("=" * 55)

    try:
        resultado = operacion()

    except Exception as error:
        print(f"ERROR CONTROLADO: {error}")
        registrar_error(descripcion, error)

    else:
        print(resultado)
        registrar_evento(f"Operacion {numero} realizada correctamente.")

    finally:
        print("Fin de la operacion.")


def iniciar_sistema():

    sistema = SistemaGestion()

    print("=" * 55)
    print("       SISTEMA INTEGRAL DE GESTION SOFTWARE FJ")
    print("=" * 55)

    # -------------------------------------------------
    # OPERACION 1: REGISTRO DE CLIENTE VALIDO
    # -------------------------------------------------

    ejecutar_prueba(
        1,
        "Registro de cliente valido",
        lambda: sistema.registrar_cliente(
            Cliente(
                "1098765432",
                "Carlos Ramirez",
                "carlos@gmail.com",
                "3001234567"
            )
        )
    )

    # -------------------------------------------------
    # OPERACION 2: REGISTRO DE OTRO CLIENTE
    # -------------------------------------------------

    ejecutar_prueba(
        2,
        "Registro de un segundo cliente",
        lambda: sistema.registrar_cliente(
            Cliente(
                "1023456789",
                "Laura Martinez",
                "laura@gmail.com",
                "3107654321"
            )
        )
    )

    # -------------------------------------------------
    # OPERACION 3: REGISTRO DE CLIENTE INVALIDO
    # -------------------------------------------------

    ejecutar_prueba(
        3,
        "Registro de cliente con correo invalido",
        lambda: sistema.registrar_cliente(
            Cliente(
                "1000000000",
                "Pedro Gomez",
                "correo_invalido",
                "3009876543"
            )
        )
    )

    # -------------------------------------------------
    # OPERACION 4: REGISTRO DE SALA
    # -------------------------------------------------

    ejecutar_prueba(
        4,
        "Registro de servicio de reserva de sala",
        lambda: sistema.registrar_servicio(
            ReservaSala(
                "S001",
                "Sala de reuniones",
                50000,
                20
            )
        )
    )

    # -------------------------------------------------
    # OPERACION 5: REGISTRO DE ALQUILER DE EQUIPOS
    # -------------------------------------------------

    ejecutar_prueba(
        5,
        "Registro de servicio de alquiler de equipos",
        lambda: sistema.registrar_servicio(
            AlquilerEquipo(
                "S002",
                "Computadores",
                15000,
                3
            )
        )
    )

    # -------------------------------------------------
    # OPERACION 6: REGISTRO DE ASESORIA
    # -------------------------------------------------

    ejecutar_prueba(
        6,
        "Registro de servicio de asesoria",
        lambda: sistema.registrar_servicio(
            Asesoria(
                "S003",
                "Asesoria informatica",
                80000,
                "Desarrollo de software"
            )
        )
    )

    # -------------------------------------------------
    # OPERACION 7: CREACION DE RESERVA VALIDA
    # -------------------------------------------------

    ejecutar_prueba(
        7,
        "Creacion de una reserva valida",
        lambda: sistema.crear_reserva(
            "R001",
            "1098765432",
            "S001",
            2,
            19,
            5
        ).obtener_informacion()
    )

    # -------------------------------------------------
    # OPERACION 8: CONFIRMACION DE RESERVA
    # -------------------------------------------------

    ejecutar_prueba(
        8,
        "Confirmacion de reserva",
        lambda: sistema.confirmar_reserva("R001")
    )

    # -------------------------------------------------
    # OPERACION 9: PROCESAMIENTO DE RESERVA
    # -------------------------------------------------

    ejecutar_prueba(
        9,
        "Procesamiento de reserva",
        lambda: sistema.procesar_reserva("R001")
    )

    # -------------------------------------------------
    # OPERACION 10: BUSQUEDA DE CLIENTE INEXISTENTE
    # -------------------------------------------------

    ejecutar_prueba(
        10,
        "Busqueda de cliente inexistente",
        lambda: sistema.buscar_cliente("9999999999")
    )

    # -------------------------------------------------
    # OPERACION 11: CREACION DE RESERVA CON DURACION INVALIDA
    # -------------------------------------------------

    ejecutar_prueba(
        11,
        "Creacion de reserva con duracion invalida",
        lambda: sistema.crear_reserva(
            "R002",
            "1098765432",
            "S002",
            -3
        )
    )

    # -------------------------------------------------
    # OPERACION 12: SERVICIO NO DISPONIBLE
    # -------------------------------------------------

    ejecutar_prueba(
        12,
        "Intento de reservar un servicio no disponible",
        lambda: intentar_servicio_no_disponible(sistema)
    )

    # -------------------------------------------------
    # OPERACION 13: CANCELACION DE RESERVA
    # -------------------------------------------------

    ejecutar_prueba(
        13,
        "Cancelacion de una reserva",
        lambda: cancelar_reserva_prueba(sistema)
    )

    # -------------------------------------------------
    # INFORMACION FINAL
    # -------------------------------------------------

    print("\n" + "=" * 55)
    print("RESUMEN FINAL DEL SISTEMA")
    print("=" * 55)

    print("\nCLIENTES REGISTRADOS:")
    for cliente in sistema.listar_clientes():
        print(cliente)
        print("-" * 30)

    print("\nSERVICIOS REGISTRADOS:")
    for servicio in sistema.listar_servicios():
        print(servicio)
        print("-" * 30)

    print("\nRESERVAS REGISTRADAS:")
    for reserva in sistema.listar_reservas():
        print(reserva)
        print("-" * 30)

    print("\nSistema finalizado correctamente.")
    print("Consulte el archivo logs.txt para ver los registros.")


def intentar_servicio_no_disponible(sistema):
    servicio = sistema.buscar_servicio("S002")
    servicio.cambiar_disponibilidad(False)

    return sistema.crear_reserva(
        "R003",
        "1098765432",
        "S002",
        2
    ).confirmar()


def cancelar_reserva_prueba(sistema):
    sistema.crear_reserva(
        "R004",
        "1023456789",
        "S003",
        1
    )

    return sistema.cancelar_reserva("R004")


if __name__ == "__main__":
    iniciar_sistema()
