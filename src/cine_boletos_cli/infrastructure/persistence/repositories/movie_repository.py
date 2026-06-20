import json
from pathlib import Path

from cine_boletos_cli.domain.entities.movie import Movie


class MovieRepository:
    """
    Repositorio de películas con persistencia JSON.
    """

    def __init__(
        self,
        file_path="data/movies.json",
    ):
        self.file_path = Path(file_path)
        self._storage = {}

        self._ensure_file_exists()
        self._load()

    def save(self, movie):
        """
        Guarda o actualiza una película.
        """
        self._storage[movie.movie_id] = movie
        self._persist()

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
        """
        movie = self._storage.pop(movie_id, None)

        if movie is not None:
            self._persist()

        return movie

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
        self._persist()

    def _ensure_file_exists(self):
        """
        Crea el archivo JSON si todavía no existe.
        """
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.file_path.exists():
            self.file_path.write_text(
                "[]",
                encoding="utf-8",
            )

    def _load(self):
        """
        Carga películas desde JSON.
        """
        raw_data = self.file_path.read_text(
            encoding="utf-8",
        ).strip()

        if not raw_data:
            raw_data = "[]"

        data = json.loads(raw_data)

        self._storage = {}

        for item in data:
            movie = Movie.from_dict(item)

            self._storage[movie.movie_id] = movie

    def _persist(self):
        """
        Persiste películas hacia JSON.
        """
        data = [
            movie.to_dict()
            for movie in self._storage.values()
        ]

        self.file_path.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )