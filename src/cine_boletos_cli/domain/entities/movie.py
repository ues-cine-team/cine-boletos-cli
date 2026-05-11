"""
Este archivo define la entidad Movie.

¿Por qué existe?
Porque el sistema necesita representar una película de forma formal y consistente.
Una función (Showtime) siempre estará asociada a una película, así que no conviene
manejar este dato como un string suelto o un diccionario genérico.

¿Cómo se usará más adelante?
- `showtime.py` usará Movie para saber qué película se proyecta.
- `movie_service.py` permitirá crear, actualizar, consultar y desactivar películas.
- `movie_repository.py` guardará y recuperará películas.
- `showtime_service.py` usará Movie para validar que una función solo se cree sobre
  una película válida y activa.

Qué debe resolver esta entidad:
- representar una película del catálogo,
- mantener su información básica,
- validar datos importantes,
- controlar su estado,
- servir como base para programar funciones.

Importante:
Movie NO debe encargarse de reservas, pagos, locks, base de datos ni consola.
Solo debe contener la lógica del dominio relacionada con películas.
"""

from datetime import datetime
from typing import Optional


class Movie:
    """
    Entidad del dominio que representa una película dentro del sistema.
    """

    def __init__(
        self,
        movie_id,
        title,
        duration_minutes,
        rating,
        genre,
        description,
        status,
        release_date: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        """
        Inicializa una película con sus datos principales.

        Args:
            movie_id:
                Identificador formal de la película.

            title:
                Título oficial de la película.

            duration_minutes:
                Duración total en minutos.

            rating:
                Clasificación por edad o categoría.
                Ejemplos: PG, PG-13, R, etc.

            genre:
                Género principal de la película.

            description:
                Sinopsis o descripción corta.

            status:
                Estado actual de la película.
                Ejemplos:
                - ACTIVE
                - UPCOMING
                - ARCHIVED

            release_date:
                Fecha oficial de estreno.

            created_at:
                Fecha de creación del registro.

            updated_at:
                Fecha de última actualización.
        """
        self.movie_id = movie_id
        self.title = title
        self.duration_minutes = duration_minutes
        self.rating = rating
        self.genre = genre
        self.description = description
        self.status = status
        self.release_date = release_date
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or self.created_at

    def is_active(self):
        """
        Indica si la película puede usarse para crear nuevas funciones.

        Debe devolver True solo si la película está habilitada para venta.
        """
        pass

    def archive(self):
        """
        Marca la película como archivada.

        Esto se usa cuando la película ya no debe seguir apareciendo
        como una opción activa para nuevas funciones.
        """
        pass

    def rename(self, new_title):
        """
        Cambia el título oficial de la película.

        Debe validar que el nuevo título:
        - no esté vacío,
        - tenga un formato razonable,
        - y cumpla las reglas del negocio.
        """
        pass

    def update_description(self, new_description):
        """
        Actualiza la descripción o sinopsis de la película.

        Este método permite mejorar o corregir la información del catálogo.
        """
        pass

    def validate_duration(self):
        """
        Valida que la duración de la película sea correcta.

        Debe impedir duraciones inválidas, como:
        - cero,
        - negativas,
        - o valores absurdamente fuera de rango.
        """
        pass

    def validate_transition(self, new_status):
        """
        Valida si el cambio de estado solicitado es permitido.

        Ejemplos esperados:
        - UPCOMING -> ACTIVE
        - ACTIVE -> ARCHIVED

        Cualquier transición inválida debe rechazarse.
        """
        pass