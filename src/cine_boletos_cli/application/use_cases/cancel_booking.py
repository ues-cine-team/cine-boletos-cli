"""
CancelBookingUseCase.

Este caso de uso representa la operación completa de cancelar una reserva o una
compra dentro del sistema.

¿Por qué existe?
----------------
Porque cancelar una reserva real no significa solamente cambiar un estado.

Una cancelación puede implicar:
- liberar asientos,
- revertir locks,
- ejecutar refunds,
- actualizar bookings,
- registrar compensaciones,
- mantener consistencia del sistema.

Este caso de uso coordina todo ese flujo de manera segura y consistente.

Relación con otros módulos
--------------------------
Este caso de uso trabajará junto con:

- `BookingService`
    Para cancelar la reserva y actualizar su estado.

- `SeatService`
    Para liberar los asientos asociados.

- `PaymentService`
    Para coordinar refunds cuando sea necesario.

- `UnitOfWork`
    Para mantener consistencia transaccional.

- `Workers`
    Más adelante podrían ejecutar compensaciones automáticas o tareas
    asincrónicas relacionadas con cancelaciones.

Qué debe resolver este caso de uso
----------------------------------
- recuperar bookings,
- validar cancelaciones,
- liberar recursos,
- coordinar refunds,
- actualizar estados,
- manejar rollback lógico,
- mantener consistencia.

Qué NO debe hacer
-----------------
- No debe imprimir mensajes para usuarios.
- No debe contener SQL directo.
- No debe manejar infraestructura concreta.
- No debe contener reglas internas de Seat o Booking.
- No debe reemplazar PaymentService.

La lógica del dominio vive en las entidades.
La coordinación de cancelación vive aquí.

Ejemplo mental
--------------
1. el usuario solicita cancelar una compra,
2. el sistema recupera el booking,
3. valida que pueda cancelarse,
4. libera asientos,
5. ejecuta refund si corresponde,
6. actualiza estados,
7. persiste cambios.

Problemas que ayuda a evitar
----------------------------
SIN coordinación:
- asientos bloqueados permanentemente,
- refunds inconsistentes,
- bookings cancelados parcialmente,
- pérdida de consistencia.

CON este caso de uso:
- la cancelación permanece controlada y recuperable.

Este archivo debe dejar clara la intención arquitectónica del flujo de
cancelación para el equipo.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class CancelBookingRequest:
    """
    Request de entrada para cancelar un booking.

    Parameters
    ----------
    booking_id : str
        Identificador del booking.

    reason : str, optional
        Motivo de cancelación.

    refund_payment : bool, default=True
        Indica si debe intentarse un refund.
    """

    booking_id: str
    reason: Optional[str] = None
    refund_payment: bool = True


class CancelBookingUseCase:
    """
    Caso de uso encargado de coordinar cancelaciones.

    Notes
    -----
    Esta clase deja definido el flujo conceptual y las responsabilidades del
    caso de uso para que el equipo implemente la lógica concreta más adelante.
    """

    def __init__(
        self,
        booking_service,
        payment_service,
        seat_service,
        unit_of_work,
    ):
        """
        Inicializa el caso de uso.

        Parameters
        ----------
        booking_service : object
            Servicio encargado de bookings.

        payment_service : object
            Servicio encargado de pagos y refunds.

        seat_service : object
            Servicio encargado de asientos.

        unit_of_work : object
            Coordinador transaccional.
        """
        self.booking_service = booking_service
        self.payment_service = payment_service
        self.seat_service = seat_service
        self.unit_of_work = unit_of_work

    def execute(self, request: CancelBookingRequest):
        """
        Ejecuta la cancelación completa.

        Parameters
        ----------
        request : CancelBookingRequest
            Solicitud de cancelación.

        Returns
        -------
        Booking
            Booking cancelado.

        Notes
        -----
        El flujo real debería incluir:
        - validación de la request,
        - recuperación del booking,
        - validación de cancelación,
        - liberación de asientos,
        - refund opcional,
        - persistencia,
        - compensaciones si falla algo.
        """
        self.validate_request(request)
        return self._execute_cancellation(request)

    def validate_request(self, request: CancelBookingRequest) -> None:
        """
        Valida la solicitud de cancelación.

        Parameters
        ----------
        request : CancelBookingRequest
            Solicitud a validar.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Si la solicitud es inválida.
        """
        if request is None:
            raise ValueError("Cancel request cannot be None.")

        if not request.booking_id:
            raise ValueError("booking_id is required.")

    def _execute_cancellation(self, request: CancelBookingRequest):
        """
        Ejecuta el flujo interno de cancelación.

        Parameters
        ----------
        request : CancelBookingRequest
            Solicitud validada.

        Returns
        -------
        Booking
            Resultado final de la cancelación.
        """
        pass

    def _release_seats(self, booking):
        """
        Libera los asientos asociados al booking.

        Este método más adelante deberá:
        - desbloquear asientos,
        - sincronizar estados,
        - actualizar persistencia.
        """
        pass

    def _process_refund(self, booking, reason: Optional[str] = None):
        """
        Coordina el refund asociado a una cancelación.

        Este método podrá:
        - ejecutar refunds parciales,
        - ejecutar refunds completos,
        - registrar referencias externas,
        - coordinar compensaciones.
        """
        pass

    def _rollback_if_needed(self, booking_id: str):
        """
        Ejecuta rollback lógico si ocurre un fallo durante la cancelación.

        Más adelante este método podrá:
        - revertir cambios parciales,
        - restaurar estados,
        - registrar inconsistencias,
        - coordinar recuperación.
        """
        pass


"""
Ejemplo conceptual de flujo futuro
----------------------------------

    request = CancelBookingRequest(
        booking_id="booking-123",
        reason="Customer requested cancellation",
        refund_payment=True,
    )

    cancel_booking_use_case.execute(request)

Resultado esperado
------------------
- booking cancelado,
- asientos liberados,
- refund ejecutado si corresponde,
- sistema consistente.

Ejemplos de escenarios futuros
------------------------------
- cancelación manual del cliente,
- función cancelada por el cine,
- timeout de pago,
- compensación automática,
- rollback operacional.

Este caso de uso será una pieza importante para mantener la recuperación y la
consistencia del sistema ante errores o cancelaciones reales.
"""