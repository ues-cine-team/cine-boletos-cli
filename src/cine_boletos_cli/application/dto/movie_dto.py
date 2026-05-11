"""
MovieDTOs.

Este archivo define los Data Transfer Objects (DTOs) relacionados con películas
dentro del sistema del cine.

¿Por qué existen?
-----------------
Porque las entidades del dominio NO deberían exponerse directamente entre capas.

La entidad Movie:
- contiene reglas,
- mantiene invariantes,
- representa comportamiento del dominio,
- puede evolucionar internamente.

Pero muchas partes del sistema solamente necesitan:
- consultar datos,
- mostrar información,
- transportar estados,
- serializar respuestas.

Los DTOs resuelven exactamente eso.

Responsabilidad principal
-------------------------
Transportar información relacionada con películas de manera:
- desacoplada,
- serializable,
- explícita,
- segura,
- simple.

Relación con otros módulos
--------------------------
Estos DTOs serán utilizados por:

- `MovieService`
- `CreateMovieUseCase`
- `ShowtimeService`
- `CLI commands`
- futuras APIs
- futuros workers
- futuras respuestas HTTP

Qué deben resolver estos DTOs
-----------------------------
- mover información entre capas,
- representar catálogo,
- simplificar respuestas,
- desacoplar presentación del dominio,
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
    objeto vivo con comportamiento.

DTO:
    snapshot simple de datos.

Problemas reales que ayudan a evitar
------------------------------------
SIN DTOs:
- acoplamiento fuerte,
- exposición accidental del dominio,
- dependencias difíciles,
- problemas de serialización.

CON DTOs:
- las capas permanecen limpias y desacopladas.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class MovieDTO:
    """
    DTO principal de películas.

    Parameters
    ----------
    movie_id : str
        Identificador de la película.

    title : str
        Nombre oficial.

    duration_minutes : int
        Duración oficial.

    classification : str
        Clasificación de contenido.

    description : str, optional
        Sinopsis.

    language : str, optional
        Idioma principal.

    genre : str, optional
        Género cinematográfico.

    is_active : bool
        Indica si la película está habilitada.

    created_at : datetime, optional
        Fecha de registro.
    """

    movie_id: str
    title: str
    duration_minutes: int
    classification: str
    description: Optional[str] = None
    language: Optional[str] = None
    genre: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None

    @property
    def duration_hours(self) -> float:
        """
        Devuelve duración aproximada en horas.

        Returns
        -------
        float
            Duración convertida.

        Notes
        -----
        Esta propiedad es aceptable porque:
        - no contiene lógica del dominio,
        - solamente transforma datos simples.
        """
        return round(self.duration_minutes / 60, 2)


@dataclass(slots=True)
class CreateMovieResponseDTO:
    """
    DTO de respuesta para creación de películas.

    Parameters
    ----------
    success : bool
        Resultado de la operación.

    movie : MovieDTO, optional
        Película creada.

    message : str, optional
        Información adicional.
    """

    success: bool
    movie: Optional[MovieDTO] = None
    message: Optional[str] = None


@dataclass(slots=True)
class MovieCatalogItemDTO:
    """
    DTO simplificado para catálogo/cartelera.

    Parameters
    ----------
    movie_id : str
        Identificador.

    title : str
        Nombre visible.

    classification : str
        Clasificación.

    duration_minutes : int
        Duración oficial.

    genre : str, optional
        Género principal.
    """

    movie_id: str
    title: str
    classification: str
    duration_minutes: int
    genre: Optional[str] = None


@dataclass(slots=True)
class MovieAvailabilityDTO:
    """
    DTO de disponibilidad operacional de película.

    Parameters
    ----------
    movie_id : str
        Película objetivo.

    is_active : bool
        Estado operacional.

    can_schedule_showtimes : bool
        Indica si puede programarse.

    reason : str, optional
        Explicación operacional.
    """

    movie_id: str
    is_active: bool
    can_schedule_showtimes: bool
    reason: Optional[str] = None


"""
Ejemplo conceptual futuro
-------------------------

    movie_dto = MovieDTO(
        movie_id="movie-001",
        title="Interstellar",
        duration_minutes=169,
        classification="PG-13",
        genre="Sci-Fi",
    )

Uso esperado
-------------
- catálogo de películas,
- respuestas administrativas,
- CLI,
- APIs futuras,
- serialización,
- transporte entre capas.

Importante
----------
Estos DTOs NO contienen lógica operacional.

Solamente representan:
- snapshots,
- estructuras serializables,
- intercambio de información.
"""