"""
domain_errors.py

Excepciones oficiales para las reglas de negocio del dominio.

Estas excepciones proporcionan una jerarquía consistente para representar
errores esperados del negocio. Las capas de aplicación y CLI pueden capturarlas
explícitamente y reaccionar de manera adecuada con lógica de recuperación,
mensajes al usuario o procesos de compensación.
"""


class DomainError(Exception):
    """
    Clase base para todas las excepciones del dominio.

    Todas las violaciones de reglas de negocio deberían heredar de esta clase
    para mantener consistencia en el manejo de errores dentro del sistema.

    Notes
    -----
    Se recomienda capturar :class:`DomainError` en lugar de ``Exception``
    cuando el error es esperado y proviene de la capa de dominio.
    """

    pass


class SeatNotAvailableError(DomainError):
    """
    Se lanza cuando un asiento no puede reservarse o comprarse.

    Este error cubre situaciones como:

    - el asiento ya fue comprado,
    - el asiento está bloqueado por otro usuario,
    - el asiento dejó de estar disponible.

    Parameters
    ----------
    message : str
        Descripción legible del error.
    """

    pass


class SeatAlreadyBookedError(DomainError):
    """
    Se lanza cuando se intenta operar sobre un asiento ya reservado.

    Parameters
    ----------
    message : str
        Descripción legible del error.
    """

    pass


class SeatLockedError(DomainError):
    """
    Se lanza cuando un asiento está bloqueado y no puede ser modificado
    por otro proceso o usuario.

    Parameters
    ----------
    message : str
        Descripción legible del error.
    """

    pass


class InvalidSeatStateTransitionError(DomainError):
    """
    Se lanza cuando un asiento cambia de estado de forma inválida.

    Parameters
    ----------
    message : str
        Descripción legible del error.
    """

    pass


class BookingNotFoundError(DomainError):
    """
    Se lanza cuando una reserva no existe o no puede encontrarse.

    Parameters
    ----------
    message : str
        Descripción legible del error.
    """

    pass


class BookingAlreadyCancelledError(DomainError):
    """
    Se lanza cuando se intenta cancelar una reserva ya cancelada.

    Parameters
    ----------
    message : str
        Descripción legible del error.
    """

    pass


class BookingAlreadyConfirmedError(DomainError):
    """
    Se lanza cuando se intenta confirmar una reserva ya confirmada.

    Parameters
    ----------
    message : str
        Descripción legible del error.
    """

    pass


class InvalidBookingStateError(DomainError):
    """
    Se lanza cuando una reserva se encuentra en un estado inválido para
    ejecutar la operación solicitada.

    Parameters
    ----------
    message : str
        Descripción legible del error.
    """

    pass


class PaymentFailedError(DomainError):
    """
    Se lanza cuando un pago no puede completarse correctamente.

    Parameters
    ----------
    message : str
        Descripción legible del error.
    """

    pass


class RefundFailedError(DomainError):
    """
    Se lanza cuando un reembolso falla.

    Parameters
    ----------
    message : str
        Descripción legible del error.
    """

    pass


class IdempotencyConflictError(DomainError):
    """
    Se lanza cuando una idempotency key entra en conflicto con una operación
    existente.

    Parameters
    ----------
    message : str
        Descripción legible del error.
    """

    pass

class InvalidSeatIdentifierError(DomainError):
    """
    Se lanza cuando un identificador de asiento es inválido.

    Examples
    --------
    - formato incorrecto,
    - fila vacía,
    - número inválido,
    - identificador incompleto.
    """

    pass
