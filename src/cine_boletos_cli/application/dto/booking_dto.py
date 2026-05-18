"""
BookingDTOs.

Este archivo define los Data Transfer Objects (DTOs) relacionados con reservas
(bookings) dentro del sistema del cine.

¿Por qué existen?
-----------------
Porque las entidades del dominio NO deberían viajar directamente entre capas.

Las entidades:
- contienen lógica,
- tienen reglas de negocio,
- mantienen invariantes,
- representan comportamiento real del dominio.

Pero muchas veces el sistema necesita solamente transportar datos entre:
- use cases,
- services,
- CLI,
- respuestas,
- integraciones futuras.

Ahí es donde entran los DTOs.

Responsabilidad principal
-------------------------
Transportar información de bookings de manera:
- simple,
- serializable,
- desacoplada,
- segura,
- explícita.

Relación con otros módulos
--------------------------
Estos DTOs serán utilizados por:

- `PurchaseTicketsUseCase`
- `CancelBookingUseCase`
- `BookingService`
- `CLI commands`
- futuras APIs
- futuros workers

Qué deben resolver estos DTOs
-----------------------------
- mover datos entre capas,
- evitar exponer entidades completas,
- simplificar respuestas,
- desacoplar dominio de presentación,
- facilitar serialización futura.

Qué NO deben hacer
------------------
- No deben contener lógica de negocio.
- No deben persistir datos.
- No deben ejecutar side effects.
- No deben contener comportamiento complejo.
- No deben reemplazar entidades del dominio.

Importante
----------
DTO != Entity

Entity:
    objeto vivo con reglas e invariantes.

DTO:
    contenedor simple de datos.

Problemas reales que ayudan a evitar
------------------------------------
SIN DTOs:
- acoplamiento entre capas,
- exposición accidental del dominio,
- estructuras difíciles de serializar,
- dependencias circulares.

CON DTOs:
- las capas se mantienen separadas y limpias.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass(slots=True)
class BookingSeatDTO:
    """
    Representa un asiento asociado a una reserva.

    Parameters
    ----------
    seat_id : str
        Identificador visible del asiento.

    row : str, optional
        Fila física.

    number : int, optional
        Número físico.
    """

    seat_id: str
    row: Optional[str] = None
    number: Optional[int] = None


@dataclass(slots=True)
class BookingCustomerDTO:
    """
    Información simplificada del cliente.

    Parameters
    ----------
    customer_id : str
        Identificador del cliente.

    full_name : str, optional
        Nombre visible.

    email : str, optional
        Correo asociado.
    """

    customer_id: str
    full_name: Optional[str] = None
    email: Optional[str] = None


@dataclass(slots=True)
class BookingDTO:
    """
    DTO principal de reservas.

    Este DTO será utilizado para transportar información de bookings entre
    distintas capas del sistema.

    Parameters
    ----------
    booking_id : str
        Identificador de la reserva.

    showtime_id : str
        Función asociada.

    customer : BookingCustomerDTO
        Cliente relacionado.

    seats : list[BookingSeatDTO]
        Asientos reservados.

    status : str
        Estado actual del booking.

    total_amount : float
        Monto total.

    currency : str
        Moneda asociada.

    created_at : datetime
        Fecha de creación.

    expires_at : datetime, optional
        Expiración del booking temporal.
    """

    booking_id: str
    showtime_id: str
    customer: BookingCustomerDTO
    seats: List[BookingSeatDTO] = field(default_factory=list)
    status: str = "PENDING"
    total_amount: float = 0.0
    currency: str = "USD"
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    @property
    def total_seats(self) -> int:
        """
        Devuelve la cantidad total de asientos.

        Returns
        -------
        int
            Número total de seats asociados.

        Notes
        -----
        Esta propiedad es aceptable en un DTO porque:
        - no contiene lógica de negocio,
        - solamente deriva información simple.
        """
        return len(self.seats)


@dataclass(slots=True)
class CreateBookingResponseDTO:
    """
    DTO de respuesta para creación de bookings.

    Parameters
    ----------
    success : bool
        Indica si la operación fue exitosa.

    booking : BookingDTO, optional
        Booking resultante.

    message : str, optional
        Mensaje informativo.

    payment_required : bool
        Indica si debe iniciarse flujo de pago.
    """

    success: bool
    booking: Optional[BookingDTO] = None
    message: Optional[str] = None
    payment_required: bool = True


@dataclass(slots=True)
class CancelBookingResponseDTO:
    """
    DTO de respuesta para cancelaciones.

    Parameters
    ----------
    success : bool
        Resultado de la operación.

    booking_id : str
        Reserva afectada.

    refund_triggered : bool
        Indica si se inició refund.

    message : str, optional
        Información adicional.
    """

    success: bool
    booking_id: str
    refund_triggered: bool = False
    message: Optional[str] = None


"""
Ejemplo conceptual futuro
-------------------------

    booking_dto = BookingDTO(
        booking_id="booking-001",
        showtime_id="showtime-001",
        customer=BookingCustomerDTO(
            customer_id="customer-001",
            full_name="Daniel Gomez",
        ),
        seats=[
            BookingSeatDTO(seat_id="A1"),
            BookingSeatDTO(seat_id="A2"),
        ],
        total_amount=20.0,
    )

Uso esperado
-------------
- respuestas de use cases,
- transporte entre capas,
- serialización futura,
- APIs REST futuras,
- respuestas CLI,
- eventos asincrónicos.

Importante
----------
Estos DTOs NO reemplazan entidades del dominio.

Solamente representan:
- vistas simplificadas,
- snapshots,
- estructuras de intercambio.
"""