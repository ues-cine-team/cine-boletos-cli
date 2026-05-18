"""
Este archivo centraliza las excepciones oficiales del dominio.

La idea es que el sistema use errores claros y consistentes en lugar de lanzar
mensajes genéricos o excepciones distintas en cada módulo.

Por ejemplo, si alguien intenta comprar un asiento que ya fue reservado,
el sistema debería lanzar un error específico del negocio y no simplemente:

raise Exception("Algo salió mal")

Ejemplo correcto:

raise SeatNotAvailableError(
    "The selected seat is no longer available."
)

Esto permite que otras partes del sistema puedan reaccionar correctamente:
- cancelar la operación,
- informar al usuario,
- registrar el problema,
- o ejecutar lógica de compensación.

Aunque algunas excepciones parezcan clases vacías, siguen siendo útiles porque
su valor está en el significado del tipo de error.

Por ejemplo:

except SeatNotAvailableError:

es mucho más claro y mantenible que usar:

except Exception:

La idea es que el dominio tenga errores oficiales y entendibles para todo el
equipo.
"""


class DomainError(Exception):
    """
    Clase base para todos los errores del dominio.

    Cualquier excepción relacionada con reglas del negocio debería heredar
    de esta clase para mantener consistencia en el manejo de errores.
    """
    pass


# ============================================================================
# EXAMPLE DOMAIN ERROR
# ============================================================================

class SeatNotAvailableError(DomainError):
    """
    Se lanza cuando un asiento ya no puede reservarse o comprarse.

    Ejemplo:
    - el asiento ya fue comprado,
    - el asiento está bloqueado por otro usuario,
    - o el asiento dejó de estar disponible.
    """
    pass


# ============================================================================
# FUTURE DOMAIN ERRORS
# ============================================================================

# TODO:
# - SeatAlreadyBookedError
# - SeatLockedError
# - InvalidSeatStateTransitionError
# - BookingNotFoundError
# - BookingAlreadyCancelledError
# - BookingAlreadyConfirmedError
# - InvalidBookingStateError
# - PaymentFailedError
# - RefundFailedError
# - IdempotencyConflictError