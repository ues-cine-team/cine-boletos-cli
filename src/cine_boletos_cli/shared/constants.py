"""
shared/constants.py

Constantes globales compartidas por todo el sistema.

Objetivos:
- evitar magic strings y magic numbers,
- mantener consistencia entre módulos,
- reducir errores por diferencias de escritura,
- centralizar configuraciones del sistema.

Todas las constantes deben reutilizarse desde este archivo.
"""

# ============================================================================
# SEAT STATES
# ============================================================================

# Asiento disponible para reservar o comprar.
SEAT_AVAILABLE = "AVAILABLE"

# Asiento bloqueado temporalmente durante el proceso de compra.
SEAT_LOCKED = "LOCKED"

# Asiento comprado exitosamente.
SEAT_BOOKED = "BOOKED"


# ============================================================================
# BOOKING STATES
# ============================================================================

# Reserva creada pero aún no confirmada.
BOOKING_PENDING = "PENDING"

# Reserva confirmada.
BOOKING_CONFIRMED = "CONFIRMED"

# Reserva cancelada.
BOOKING_CANCELLED = "CANCELLED"


# ============================================================================
# PAYMENT STATES
# ============================================================================

# Pago en proceso.
PAYMENT_PENDING = "PENDING"

# Pago completado exitosamente.
PAYMENT_PAID = "PAID"

# Pago fallido.
PAYMENT_FAILED = "FAILED"

# Pago reembolsado.
PAYMENT_REFUNDED = "REFUNDED"


# ============================================================================
# LOCK CONFIGURATION
# ============================================================================

# Tiempo máximo de bloqueo de asiento (segundos).
LOCK_TTL_SECONDS = 300


# ============================================================================
# SYSTEM CONFIGURATION
# ============================================================================

# Moneda por defecto del sistema.
DEFAULT_CURRENCY = "USD"

# Timezone por defecto.
DEFAULT_TIMEZONE = "UTC"

# Máximo de asientos permitidos por reserva.
MAX_SEATS_PER_BOOKING = 10