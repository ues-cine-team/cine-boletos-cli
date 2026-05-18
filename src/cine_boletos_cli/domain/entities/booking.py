"""
Este archivo define la entidad Booking.

¿Por qué existe?
Porque una compra de boletos no es solo un dato suelto. Necesitamos una entidad
que represente toda la reserva: quién la hizo, para qué función, qué asientos
incluye, cuánto cuesta y en qué estado se encuentra.

¿Cómo se usará más adelante?
- `booking_service.py` usará Booking para coordinar la compra y la cancelación.
- `payment_service.py` se apoyará en el estado del booking para saber si puede
  cobrarse, confirmarse o revertirse.
- `booking_repository.py` guardará y recuperará esta entidad.
- `seat.py` se relacionará con Booking porque un booking agrupa varios asientos.

Qué debe resolver esta entidad:
- representar una reserva o compra,
- mantener consistencia entre asientos, total y estado,
- permitir confirmar o cancelar de forma válida,
- evitar transiciones ilegales.

Estados esperados:
- PENDING: la reserva existe pero aún no está confirmada.
- CONFIRMED: el pago fue exitoso y la compra quedó cerrada.
- CANCELLED: la reserva fue anulada.

Idea importante:
Booking no debe encargarse de cobrar, guardar en base de datos ni hablar con
la consola. Solo debe contener reglas del dominio relacionadas con la reserva.
"""

from datetime import datetime
from typing import List, Optional

# Se espera que más adelante se usen los value objects oficiales.
# from cine_boletos_cli.domain.value_objects.money import Money
# from cine_boletos_cli.domain.value_objects.seat_id import SeatId


class Booking:
    """
    Entidad del dominio que representa una reserva o compra de boletos.
    """

    def __init__(
        self,
        booking_id,
        customer_id,
        showtime_id,
        seat_ids,
        total_amount,
        status,
        payment_status,
        created_at: datetime,
        updated_at: Optional[datetime] = None,
        idempotency_key: Optional[str] = None,
    ):
        """
        Inicializa un booking con sus datos principales.

        Args:
            booking_id:
                Identificador formal de la reserva.

            customer_id:
                Identificador del cliente que realizó la reserva.

            showtime_id:
                Identificador de la función asociada.

            seat_ids:
                Lista de identificadores de los asientos incluidos en la compra.

            total_amount:
                Monto total calculado para la reserva.

            status:
                Estado actual del booking.

            payment_status:
                Estado del pago asociado.

            created_at:
                Fecha y hora en que se creó la reserva.

            updated_at:
                Fecha y hora de la última actualización.

            idempotency_key:
                Clave usada para evitar duplicar operaciones.
        """
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.showtime_id = showtime_id
        self.seat_ids = seat_ids
        self.total_amount = total_amount
        self.status = status
        self.payment_status = payment_status
        self.created_at = created_at
        self.updated_at = updated_at or created_at
        self.idempotency_key = idempotency_key

    def calculate_total(self):
        """
        Calcula o devuelve el total de la reserva.

        Más adelante este método puede apoyarse en:
        - precio base de la función,
        - cantidad de asientos,
        - descuentos o recargos.

        Por ahora solo deja clara la intención del método.
        """
        pass

    def confirm(self):
        """
        Confirma la reserva.

        Debe:
        - validar que el booking esté en un estado que permita confirmación,
        - cambiar el estado a CONFIRMED,
        - marcar el pago como exitoso si corresponde.

        Si el booking ya fue cancelado o no está listo, debe rechazar la acción.
        """
        pass

    def cancel(self):
        """
        Cancela la reserva.

        Debe:
        - validar que todavía se pueda cancelar,
        - cambiar el estado a CANCELLED,
        - dejar listo al sistema para liberar asientos o compensar si hace falta.
        """
        pass

    def mark_payment_pending(self):
        """
        Marca el pago como pendiente.

        Se usa cuando la reserva ya existe pero el pago todavía no fue confirmado.
        """
        pass

    def mark_paid(self):
        """
        Marca el pago como completado.
        """
        pass

    def mark_failed(self):
        """
        Marca el pago como fallido.
        """
        pass

    def is_cancellable(self):
        """
        Indica si el booking todavía puede cancelarse.

        Más adelante esta lógica dependerá del estado actual de la reserva.
        """
        pass

    def validate_transition(self, new_status):
        """
        Valida si el cambio de estado es permitido.

        Ejemplos esperados:
        - PENDING -> CONFIRMED
        - PENDING -> CANCELLED

        Cambios inválidos deben rechazarse para no romper la consistencia.
        """
        pass