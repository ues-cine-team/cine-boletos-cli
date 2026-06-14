class MovieRepository:
    """
    Repositorio de películas en memoria.
    Usa un diccionario interno para simular persistencia.
    """

    def __init__(self):
        self._storage = {}

    def save(self, movie):
        """
        Guarda o actualiza una película.
        """
        self._storage[movie.movie_id] = movie
        return movie

    def get_by_id(self, movie_id):
        """
        Recupera una película por id.
        """
        return self._storage.get(movie_id)

    def exists(self, movie_id):
        """
        Verifica si una película existe.
        """
        return movie_id in self._storage

    def list_all(self):
        """
        Devuelve todo el catálogo.
        """
        return list(self._storage.values())

    def list_active(self):
        """
        Devuelve únicamente películas activas.
        """
        return [
            movie
            for movie in self._storage.values()
            if movie.is_active()
        ]

    def search_by_title(self, title):
        """
        Busca películas por coincidencia parcial de título.
        """
        title_lower = title.lower()

        return [
            movie
            for movie in self._storage.values()
            if title_lower in movie.title.lower()
        ]

    def delete(self, movie_id):
        """
        Elimina una película.

        Returns
        -------
        Movie | None
            Película eliminada o None.
        """
        return self._storage.pop(movie_id, None)

    def count(self):
        """
        Devuelve la cantidad total de películas.
        """
        return len(self._storage)

    def clear(self):
        """
        Limpia completamente el repositorio.
        Útil para pruebas.
        """
        self._storage.clear()