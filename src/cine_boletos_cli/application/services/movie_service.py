"""
MovieService.

Este servicio coordina las operaciones relacionadas con películas dentro del
sistema del cine.

¿Por qué existe?
----------------
Porque una película no es solamente un registro almacenado en una base de datos.

Una película dentro del sistema representa:
- contenido disponible para cartelera,
- duración oficial,
- clasificación,
- disponibilidad operacional,
- relación con funciones,
- estado dentro del catálogo.

Este servicio coordina esas operaciones sin mezclar:
- reglas del dominio,
- persistencia,
- infraestructura,
- ni detalles de interfaz.

Responsabilidad principal
-------------------------
Coordinar operaciones relacionadas con:

- creación de películas,
- activación/desactivación,
- validación de disponibilidad,
- acceso al catálogo,
- consulta de cartelera,
- validaciones operacionales.

Relación con otros módulos
--------------------------
Este servicio trabajará junto con:

- `MovieRepository`
    Persistencia de películas.

- `ShowtimeRepository`
    Validaciones relacionadas con funciones activas.

- `Movie`
    Entidad principal del dominio.

- `create_movie.py`
    Caso de uso encargado de registrar películas.

- `ShowtimeService`
    Para validar programación de funciones.

Qué debe resolver este servicio
-------------------------------
- crear películas válidas,
- validar disponibilidad,
- controlar activación/desactivación,
- consultar cartelera,
- impedir operaciones inconsistentes.

Qué NO debe hacer
-----------------
- No debe manejar pagos.
- No debe manejar asientos.
- No debe manejar horarios directamente.
- No debe imprimir mensajes.
- No debe contener SQL.
- No debe actuar como CRUD genérico.

La lógica interna de Movie pertenece a la entidad.
La coordinación operacional pertenece aquí.

Problemas reales que ayuda a evitar
-----------------------------------
SIN este servicio:
- películas inválidas,
- películas sin estado operacional,
- funciones creadas sobre películas inactivas,
- inconsistencias de catálogo.

CON este servicio:
- el catálogo permanece consistente y controlado.

Importante
----------
Este servicio NO debe diseñarse como CRUD puro.

NO:
    create()
    update()
    delete()

SÍ:
    create_movie()
    activate_movie()
    deactivate_movie()
    list_now_showing()

Porque expresa operaciones reales del negocio.
"""

from __future__ import annotations

from typing import Iterable, Optional


class MovieService:
    """
    Servicio encargado de coordinar operaciones sobre películas.

    Notes
    -----
    Esta clase deja definida la estructura operacional del catálogo de películas
    para que el equipo implemente posteriormente la lógica concreta.
    """

    def __init__(
        self,
        movie_repository,
        showtime_repository=None,
    ):
        """
        Inicializa el servicio.

        Parameters
        ----------
        movie_repository : object
            Repositorio de películas.

        showtime_repository : object, optional
            Repositorio de funciones.

            Puede utilizarse más adelante para validar relaciones entre
            películas y funciones activas.
        """
        self.movie_repository = movie_repository
        self.showtime_repository = showtime_repository

    def create_movie(
        self,
        title: str,
        duration_minutes: int,
        classification: str,
        description: Optional[str] = None,
    ):
        """
        Crea una nueva película.

        Este método deberá:
        - validar datos mínimos,
        - validar duración,
        - construir la entidad Movie,
        - persistir la película,
        - devolver el resultado.

        Parameters
        ----------
        title : str
            Nombre oficial de la película.

        duration_minutes : int
            Duración oficial en minutos.

        classification : str
            Clasificación de contenido.

        description : str, optional
            Descripción o sinopsis.

        Returns
        -------
        Movie
            Película creada.
        """
        pass

    def get_movie_by_id(self, movie_id: str):
        """
        Recupera una película por su identificador.

        Parameters
        ----------
        movie_id : str
            Identificador de la película.

        Returns
        -------
        Movie | None
            Película encontrada.
        """
        pass

    def list_now_showing(self) -> Iterable:
        """
        Lista películas actualmente activas en cartelera.

        Returns
        -------
        Iterable[Movie]
            Películas disponibles para programación y venta.
        """
        pass

    def activate_movie(self, movie_id: str):
        """
        Activa una película dentro del catálogo.

        Una película activa podrá:
        - aparecer en cartelera,
        - programarse en funciones,
        - utilizarse operacionalmente.

        Parameters
        ----------
        movie_id : str
            Película a activar.

        Returns
        -------
        Movie
            Película activada.
        """
        pass

    def deactivate_movie(
        self,
        movie_id: str,
        reason: Optional[str] = None,
    ):
        """
        Desactiva una película del catálogo.

        Este método podrá utilizarse cuando:
        - una película salga de cartelera,
        - existan problemas operacionales,
        - se desee impedir nuevas funciones.

        Parameters
        ----------
        movie_id : str
            Película objetivo.

        reason : str, optional
            Motivo de desactivación.

        Returns
        -------
        Movie
            Película desactivada.
        """
        pass

    def can_schedule_showtimes(self, movie_id: str) -> bool:
        """
        Determina si una película puede programarse en funciones.

        Este método deberá validar:
        - existencia,
        - estado activo,
        - restricciones operacionales.

        Parameters
        ----------
        movie_id : str
            Película a validar.

        Returns
        -------
        bool
            True si puede utilizarse en funciones.
        """
        pass

    def validate_movie_data(
        self,
        title: str,
        duration_minutes: int,
        classification: str,
    ) -> None:
        """
        Valida datos básicos de una película.

        Parameters
        ----------
        title : str
            Nombre de la película.

        duration_minutes : int
            Duración oficial.

        classification : str
            Clasificación.

        Raises
        ------
        ValueError
            Si los datos son inválidos.
        """
        if not title:
            raise ValueError("Movie title is required.")

        if duration_minutes <= 0:
            raise ValueError("Movie duration must be greater than zero.")

        if not classification:
            raise ValueError("Movie classification is required.")


"""
Ejemplo conceptual futuro
-------------------------

    movie_service.create_movie(
        title="Interstellar",
        duration_minutes=169,
        classification="PG-13",
    )

Flujo esperado
--------------
1. validar datos,
2. construir entidad Movie,
3. persistir película,
4. devolver resultado.

Escenarios reales futuros
-------------------------
- películas activas/inactivas,
- cartelera actual,
- restricciones operacionales,
- validaciones de programación,
- relación con funciones.

Este servicio será la capa operacional encargada de mantener consistente el
catálogo de películas del sistema.
"""