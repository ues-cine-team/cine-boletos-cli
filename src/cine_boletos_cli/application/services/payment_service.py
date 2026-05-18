"""
PaymentService.

Este servicio coordina el ciclo de pagos dentro del sistema de boletos.

¿Por qué existe?
----------------
Porque el proceso de pago no debe mezclarse directamente con:
- la lógica de asientos,
- la lógica de bookings,
- la CLI,
- ni la infraestructura externa.

El sistema necesita una capa especializada que coordine:
- pagos exitosos,
- pagos fallidos,
- confirmaciones,
- reembolsos,
- consistencia transaccional,
- integración con gateways externos.

`PaymentService` representa esa capa.

Importante
-----------
Este servicio NO es Stripe, PayPal o un banco.

Este servicio representa:
- la lógica de pagos DEL SISTEMA.

Más adelante podrá conectarse con:
- Stripe,
- PayPal,
- Adyen,
- MercadoPago,
- APIs bancarias,
- simuladores de pago.

Relación con otros módulos
--------------------------
- `BookingService`
    Usará este servicio para procesar compras.

- `Booking`
    Cambiará estados de pago:
    PENDING -> PAID -> FAILED -> REFUNDED

- `SeatService`
    Puede liberar asientos cuando un pago falla.

- `UnitOfWork`
    Garantiza consistencia durante operaciones críticas.

- `IdempotencyService`
    Ayuda a evitar cobros duplicados.

- `Workers`
    Podrán ejecutar:
    - reintentos,
    - compensaciones,
    - conciliaciones,
    - refunds automáticos.

Qué debe resolver este servicio
-------------------------------
- iniciar pagos,
- validar pagos,
- confirmar transacciones,
- registrar fallos,
- coordinar reembolsos,
- mantener consistencia,
- evitar operaciones duplicadas,
- coordinar compensaciones.

Qué NO debe hacer
-----------------
- No debe imprimir mensajes para usuarios.
- No debe manejar CLI.
- No debe contener SQL directo.
- No debe contener lógica de negocio de Booking o Seat.
- No debe acoplarse a un proveedor específico.

La lógica del flujo de pago vive aquí.
La integración técnica concreta vivirá en infraestructura.

Ejemplo conceptual
------------------

1. el usuario intenta pagar,
2. el sistema inicia transacción,
3. el gateway responde,
4. si el pago funciona:
       booking confirmado,
       asientos confirmados,
5. si falla:
       locks liberados,
       booking cancelado.

Problemas que ayuda a evitar
----------------------------
SIN este servicio:
- pagos duplicados,
- bookings inconsistentes,
- asientos vendidos sin cobro,
- cobros sin reserva,
- rollback incompleto.

CON PaymentService:
- el flujo financiero permanece coordinado y consistente.

Este archivo debe actuar como núcleo de coordinación del flujo de pagos.
"""

from __future__ import annotations

from typing import Optional


class PaymentService:
    """
    Servicio encargado de coordinar pagos del sistema.

    Parameters
    ----------
    booking_repository : object
        Repositorio encargado de bookings.

    seat_service : object
        Servicio encargado de operaciones sobre asientos.

    idempotency_service : object
        Servicio encargado de prevenir operaciones duplicadas.

    unit_of_work : object
        Coordinador transaccional del sistema.

    Notes
    -----
    Esta clase NO representa un gateway concreto.

    Más adelante podrá integrarse con:
    - Stripe,
    - PayPal,
    - APIs bancarias,
    - simuladores de pago.
    """

    def __init__(
        self,
        booking_repository,
        seat_service,
        idempotency_service,
        unit_of_work,
    ):
        self.booking_repository = booking_repository
        self.seat_service = seat_service
        self.idempotency_service = idempotency_service
        self.unit_of_work = unit_of_work

    def process_payment(
        self,
        booking_id: str,
        payment_method: str,
        amount,
        idempotency_key: Optional[str] = None,
    ):
        """
        Inicia el procesamiento de un pago.

        Este método deberá:

        1. validar booking,
        2. validar estado,
        3. verificar idempotencia,
        4. iniciar operación de pago,
        5. registrar resultado,
        6. coordinar rollback si falla.

        Parameters
        ----------
        booking_id : str
            Identificador del booking.

        payment_method : str
            Método de pago solicitado.

        amount : Money
            Monto esperado del pago.

        idempotency_key : str, optional
            Clave para evitar pagos duplicados.

        Returns
        -------
        PaymentResult
            Resultado conceptual del pago.
        """
        pass

    def confirm_payment(
        self,
        booking_id: str,
        payment_reference: Optional[str] = None,
    ):
        """
        Marca un pago como exitoso.

        Este método deberá:

        1. recuperar booking,
        2. validar estado,
        3. confirmar compra,
        4. confirmar asientos,
        5. persistir cambios.

        Parameters
        ----------
        booking_id : str
            Identificador del booking.

        payment_reference : str, optional
            Referencia externa del gateway.

        Returns
        -------
        Booking
            Booking confirmado como pagado.
        """
        pass

    def fail_payment(
        self,
        booking_id: str,
        reason: Optional[str] = None,
    ):
        """
        Maneja un pago fallido.

        Este método deberá:

        1. recuperar booking,
        2. registrar fallo,
        3. liberar locks,
        4. cancelar operación,
        5. persistir cambios.

        Parameters
        ----------
        booking_id : str
            Identificador del booking.

        reason : str, optional
            Motivo del fallo.

        Returns
        -------
        Booking
            Booking actualizado tras el fallo.
        """
        pass

    def refund_payment(
        self,
        booking_id: str,
        reason: Optional[str] = None,
    ):
        """
        Ejecuta un reembolso.

        Este método deberá:

        1. validar elegibilidad,
        2. coordinar refund externo,
        3. actualizar estados,
        4. persistir cambios.

        Parameters
        ----------
        booking_id : str
            Identificador del booking.

        reason : str, optional
            Motivo del refund.

        Returns
        -------
        Booking
            Booking actualizado tras el refund.
        """
        pass

    def get_payment_status(
        self,
        booking_id: str,
    ):
        """
        Obtiene el estado de pago de un booking.

        Parameters
        ----------
        booking_id : str
            Identificador del booking.

        Returns
        -------
        str
            Estado conceptual del pago.

        Examples
        --------
        - PENDING
        - PAID
        - FAILED
        - REFUNDED
        """
        pass

    def validate_payment(
        self,
        booking_id: str,
        amount,
    ) -> None:
        """
        Valida que un pago pueda ejecutarse.

        Este método deberá verificar:
        - existencia del booking,
        - estado válido,
        - monto correcto,
        - elegibilidad,
        - integridad de la operación.

        Parameters
        ----------
        booking_id : str
            Identificador del booking.

        amount : Money
            Monto esperado.

        Returns
        -------
        None
        """
        pass


"""
Ejemplo conceptual de flujo futuro
----------------------------------

    payment_service.process_payment(
        booking_id="booking-123",
        payment_method="credit_card",
        amount=Money(amount=20_00, currency="USD"),
        idempotency_key="payment-abc-123",
    )

Si el gateway responde correctamente:

    payment_service.confirm_payment(
        booking_id="booking-123",
        payment_reference="stripe-456",
    )

Si el pago falla:

    payment_service.fail_payment(
        booking_id="booking-123",
        reason="Card declined",
    )

Ejemplo conceptual de refund
----------------------------

    payment_service.refund_payment(
        booking_id="booking-123",
        reason="Show cancelled",
    )

Problemas que este servicio ayuda a evitar
------------------------------------------
SIN coordinación de pagos:
- cobros duplicados,
- pagos inconsistentes,
- compras parcialmente completadas,
- asientos retenidos indefinidamente,
- pérdida de consistencia financiera.

CON PaymentService:
- el flujo financiero permanece controlado y recuperable.
"""