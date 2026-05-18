"""
ShowtimeDTOs.

Este archivo define los Data Transfer Objects (DTOs) relacionados con funciones
(showtimes) dentro del sistema del cine.

¿Por qué existen?
-----------------
Porque las entidades del dominio NO deberían viajar directamente entre capas.

La entidad Showtime:
- contiene comportamiento,
- mantiene reglas temporales,
- coordina disponibilidad,
- representa lógica operacional.

Pero muchas partes del sistema solamente necesitan:
- consultar horarios,
- mostrar cartelera,
- transportar disponibilidad,
- serializar respuestas,
- exponer información simplificada.

Los DTOs permiten exactamente eso.

Responsabilidad principal
-------------------------
Transportar información relacionada con funciones de manera:
- desacoplada,
- simple,
- serializable,
- explícita,
- segura.

Relación con otros módulos
--------------------------
Estos DTOs serán utilizados por:

- `ShowtimeService`
- `CreateShowtimeUseCase`
- `PurchaseTicketsUseCase`
- `CLI commands`
- futuras APIs
- futuros workers
- respuestas administrativas.

Qué deben resolver estos DTOs
-----------------------------
- mover información entre capas,
- representar cartelera,
- representar disponibilidad,
- desacoplar dominio de presentación,
- facilitar serialización futura.

Qué NO deben hacer
------------------
- No deben contener lógica de negocio.
- No deben modificar entidades.
- No deben contener persistencia.
- No deben ejecutar side effects.
- No deben reemplazar entidades del dominio.

Importante
----------
DTO != Entity

Entity:
    objeto vivo del dominio.

DTO:
    estructura simple de intercambio.

Problemas reales que ayudan a evitar
------------------------------------
SIN DTOs:
- acoplamiento entre capas,
- exposición accidental del dominio,
- serialización difícil,
- dependencias innecesarias.

CON DTOs:
- el sistema permanece limpio y modular.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class ShowtimeMovieDTO:
    """
    Información simplificada de película asociada.

    Parameters
    ----------
    movie_id : str
        Identificador de película.

    title : str
        Nombre visible.

    classification : str
        Clasificación.
    """

    movie_id: str
    title: str
    classification: str


@dataclass(slots=True)
class ShowtimeRoomDTO:
    """
    Información simplificada de sala.

    Parameters
    ----------
    room_id : str
        Identificador de sala.

    room_name : str
        Nombre visible.

    capacity : int
        Capacidad total.
    """

    room_id: str
    room_name: str
    capacity: int


@dataclass(slots=True)
class ShowtimeAvailabilityDTO:
    """
    Información de disponibilidad de seats.

    Parameters
    ----------
    total_seats : int
        Total de asientos.

    available_seats : int
        Seats disponibles.

    locked_seats : int
        Seats temporalmente bloqueados.

    booked_seats : int
        Seats vendidos.
    """

    total_seats: int
    available_seats: int
    locked_seats: int
    booked_seats: int

    @property
    def occupancy_percentage(self) -> float:
        """
        Devuelve porcentaje aproximado de ocupación.

        Returns
        -------
        float
            Porcentaje calculado.

        Notes
        -----
        Esta propiedad es aceptable porque:
        - no altera estado,
        - no contiene reglas complejas,
        - solamente deriva información simple.
        """
        if self.total_seats == 0:
            return 0.0

        return round(
            (self.booked_seats / self.total_seats) * 100,
            2,
        )


@dataclass(slots=True)
class ShowtimeDTO:
    """
    DTO principal de funciones.

    Parameters
    ----------
    showtime_id : str
        Identificador de función.

    movie : ShowtimeMovieDTO
        Película asociada.

    room : ShowtimeRoomDTO
        Sala asociada.

    starts_at : datetime
        Hora de inicio.

    ends_at : datetime, optional
        Hora estimada de finalización.

    language : str, optional
        Idioma.

    format_type : str, optional
        Formato de proyección.

    status : str
        Estado operacional.

    availability : ShowtimeAvailabilityDTO, optional
        Información de disponibilidad.
    """

    showtime_id: str
    movie: ShowtimeMovieDTO
    room: ShowtimeRoomDTO
    starts_at: datetime
    ends_at: Optional[datetime] = None
    language: Optional[str] = None
    format_type: Optional[str] = None
    status: str = "SCHEDULED"
    availability: Optional[ShowtimeAvailabilityDTO] = None

    @property
    def is_sold_out(self) -> bool:
        """
        Indica si la función está agotada.

        Returns
        -------
        bool
            True si no quedan seats disponibles.
        """
        if self.availability is None:
            return False

        return self.availability.available_seats <= 0


@dataclass(slots=True)
class CreateShowtimeResponseDTO:
    """
    DTO de respuesta para creación de funciones.

    Parameters
    ----------
    success : bool
        Resultado de la operación.

    showtime : ShowtimeDTO, optional
        Función creada.

    message : str, optional
        Información adicional.
    """

    success: bool
    showtime: Optional[ShowtimeDTO] = None
    message: Optional[str] = None


@dataclass(slots=True)
class ShowtimeScheduleItemDTO:
    """
    DTO simplificado para cartelera/programación.

    Parameters
    ----------
    showtime_id : str
        Identificador de función.

    movie_title : str
        Película visible.

    starts_at : datetime
        Inicio de función.

    room_name : str
        Sala visible.

    available_seats : int
        Seats disponibles.
    """

    showtime_id: str
    movie_title: str
    starts_at: datetime
    room_name: str
    available_seats: int


"""
Ejemplo conceptual futuro
-------------------------

    showtime_dto = ShowtimeDTO(
        showtime_id="showtime-001",
        movie=ShowtimeMovieDTO(
            movie_id="movie-001",
            title="Interstellar",
            classification="PG-13",
        ),
        room=ShowtimeRoomDTO(
            room_id="room-a",
            room_name="Sala IMAX",
            capacity=120,
        ),
        starts_at=datetime(...),
    )

Uso esperado
-------------
- cartelera,
- respuestas CLI,
- APIs futuras,
- consultas administrativas,
- serialización,
- intercambio entre capas.

Importante
----------
Estos DTOs NO contienen comportamiento del dominio.

Solamente representan:
- snapshots,
- vistas simplificadas,
- estructuras de transporte.
"""