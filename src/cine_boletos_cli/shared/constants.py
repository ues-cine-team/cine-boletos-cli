"""
Este archivo concentra los valores fijos que usa todo el sistema.

La idea es evitar escribir strings repetidos en distintos archivos, porque eso
termina generando inconsistencias y bugs difíciles de detectar.

Por ejemplo:
si un developer escribe "BOOKED" y otro escribe "booked",
ambos creen que significan lo mismo, pero Python los considera distintos.

Eso puede provocar errores como este:

seat.status = "booked"

if seat.status == "BOOKED":
    print("El asiento ya fue comprado")
else:
    print("El sistema cree que el asiento NO esta comprado")

Resultado:
el sistema podria permitir vender el mismo asiento otra vez.

Por eso los estados oficiales del sistema se definen una sola vez aquí y el
resto de módulos simplemente los reutilizan.

Ejemplo correcto:

seat.status = SEAT_BOOKED

if seat.status == SEAT_BOOKED:
    print("El asiento ya fue comprado")

De esa forma todos los developers usan exactamente los mismos valores.
"""

# ============================================================================
# SEAT STATES
# ============================================================================

# Estado de un asiento disponible para reservar o comprar.
SEAT_AVAILABLE = "AVAILABLE"

# TODO:
# SEAT_LOCKED
# SEAT_BOOKED


# ============================================================================
# BOOKING STATES
# ============================================================================

# TODO:
# BOOKING_PENDING
# BOOKING_CONFIRMED
# BOOKING_CANCELLED


# ============================================================================
# PAYMENT STATES
# ============================================================================

# TODO:
# PAYMENT_PENDING
# PAYMENT_PAID
# PAYMENT_FAILED
# PAYMENT_REFUNDED


# ============================================================================
# LOCK CONFIGURATION
# ============================================================================

# TODO:
# máximo que un asiento puede permanecer bloqueado antes de liberarse automáticamente
# LOCK_TTL_SECONDS


# ============================================================================
# SYSTEM CONFIGURATION
# ============================================================================

# TODO:
# DEFAULT_CURRENCY
# DEFAULT_TIMEZONE
# MAX_SEATS_PER_BOOKING