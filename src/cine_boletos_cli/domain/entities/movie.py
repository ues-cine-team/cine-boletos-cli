from datetime import datetime
from typing import Optional


class Movie:
    """
    Entidad del dominio que representa una película dentro del sistema.
    """

    ACTIVE = "ACTIVE"
    UPCOMING = "UPCOMING"
    ARCHIVED = "ARCHIVED"

    VALID_STATUSES = {
        ACTIVE,
        UPCOMING,
        ARCHIVED,
    }

    def __init__(
        self,
        movie_id: str,
        title: str,
        duration_minutes: int,
        classification: str,
        genre: str,
        description: str,
        status: str,
        release_date: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        if not movie_id:
            raise ValueError("movie_id cannot be empty")

        if not title or not title.strip():
            raise ValueError("title cannot be empty")

        if duration_minutes <= 0:
            raise ValueError("duration_minutes must be greater than zero")

        if duration_minutes > 500:
            raise ValueError("duration_minutes exceeds allowed limit")

        if not classification:
            raise ValueError("classification cannot be empty")

        if not genre:
            raise ValueError("genre cannot be empty")

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")

        self.movie_id = movie_id
        self.title = title.strip()
        self.duration_minutes = duration_minutes
        self.classification = classification
        self.genre = genre
        self.description = description or ""
        self.status = status
        self.release_date = release_date

        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or self.created_at

    def is_active(self) -> bool:
        """
        Indica si la película puede usarse para crear nuevas funciones.
        """
        return self.status == self.ACTIVE

    def activate(self):
        """
        Activa una película.
        """
        self.validate_transition(self.ACTIVE)

        self.status = self.ACTIVE
        self.updated_at = datetime.utcnow()

    def archive(self):
        """
        Marca la película como archivada.
        """
        self.validate_transition(self.ARCHIVED)

        self.status = self.ARCHIVED
        self.updated_at = datetime.utcnow()

    def rename(self, new_title: str):
        """
        Cambia el título oficial de la película.
        """
        if not new_title or not new_title.strip():
            raise ValueError("Title cannot be empty")

        self.title = new_title.strip()
        self.updated_at = datetime.utcnow()

    def update_description(self, new_description: str):
        """
        Actualiza la sinopsis.
        """
        self.description = new_description or ""
        self.updated_at = datetime.utcnow()

    def validate_duration(self) -> bool:
        """
        Valida duración.
        """
        if self.duration_minutes <= 0:
            raise ValueError(
                "Duration must be greater than zero"
            )

        if self.duration_minutes > 500:
            raise ValueError(
                "Duration exceeds allowed limit"
            )

        return True

    def validate_transition(self, new_status: str) -> bool:
        """
        Valida cambios de estado.
        """

        valid_transitions = {
            self.UPCOMING: [
                self.ACTIVE,
                self.ARCHIVED,
            ],
            self.ACTIVE: [
                self.ARCHIVED,
            ],
            self.ARCHIVED: [],
        }

        allowed = valid_transitions.get(
            self.status,
            [],
        )

        if new_status not in allowed:
            raise ValueError(
                f"Invalid transition: "
                f"{self.status} -> {new_status}"
            )

        return True

    def to_dict(self):
        """
        Facilita persistencia JSON futura.
        """
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "duration_minutes": self.duration_minutes,
            "classification": self.classification,
            "genre": self.genre,
            "description": self.description,
            "status": self.status,
            "release_date": (
                self.release_date.isoformat()
                if self.release_date
                else None
            ),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return (
            "Movie("
            f"movie_id={self.movie_id!r}, "
            f"title={self.title!r}, "
            f"status={self.status!r})"
        )