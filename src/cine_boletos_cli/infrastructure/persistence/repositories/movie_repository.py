"""
Este archivo define el contrato del repositorio de películas.
¿Por qué existe?
Porque la entidad Movie no debe saber cómo se guarda ni cómo se consulta desde
una base de datos. Esa responsabilidad se separa aquí para mantener el dominio
limpio y evitar mezclar reglas de negocio con detalles técnicos.
¿Cómo se usará más adelante?
- `movie_service.py` usará este repositorio para crear, actualizar y consultar películas.
- `showtime_service.py` lo usará para validar que una función se cree sobre una película válida.
- futuros módulos de cartelera o administración podrían usarlo para búsquedas y reportes.
Qué debe resolver este repositorio:
- guardar películas,
- recuperar películas por ID,
- listar películas activas,
- listar todo el catálogo,
- buscar películas por título,
- actualizar cambios de estado o metadata.
Importante:
Este archivo NO debe decidir:
- si una película puede archivarse,
- si un título es válido,
- si la duración está bien,
- ni si el cambio de estado es correcto.
Eso pertenece a la entidad Movie y a los servicios del dominio.
El repositorio solo guarda, recupera y actualiza datos.
"""


class MovieRepository:
    """
    Repositorio de películas en memoria.
    Usa un diccionario interno para simular persistencia.
    """

    def __init__(self):
        # Diccionario: movie_id -> objeto Movie
        self._storage = {}

    def save(self, movie):
        """
        Guarda o actualiza una película.

        Args:
            movie: Entidad Movie ya validada por el dominio.

        Returns:
            Movie: la película persistida.
        """
        self._storage[movie.movie_id] = movie
        return movie

    def get_by_id(self, movie_id):
        """
        Busca una película por su identificador.

        Args:
            movie_id: Identificador formal de la película.

        Returns:
            Movie | None: la película encontrada o None si no existe.
        """
        return self._storage.get(movie_id, None)

    def list_all(self):
        """
        Devuelve todas las películas del catálogo.

        Returns:
            list[Movie]: lista completa de películas.
        """
        return list(self._storage.values())

    def list_active(self):
        """
        Devuelve solo las películas activas.

        Returns:
            list[Movie]: películas activas.
        """
        return [
            movie for movie in self._storage.values()
            if getattr(movie, "is_active", False)
        ]

    def search_by_title(self, title):
        """
        Busca películas por título o coincidencia parcial.

        Args:
            title: Texto de búsqueda.

        Returns:
            list[Movie]: películas que coinciden con la búsqueda.
        """
        title_lower = title.lower()
        return [
            movie for movie in self._storage.values()
            if title_lower in getattr(movie, "title", "").lower()
        ]

    def delete(self, movie_id):
        """
        Elimina una película del almacenamiento.

        Args:
            movie_id: Identificador de la película.
        """
        if movie_id in self._storage:
            del self._storage[movie_id]
