"""
Este archivo define la entidad Showtime.

¿Por qué existe?
Porque una película sola no basta para vender boletos. El sistema necesita
saber en qué sala se proyecta, a qué hora empieza, cuánto cuesta y si sigue
activa para reservar asientos.

¿Cómo se usará más adelante?
- `showtime_service.py` usará Showtime para crear, consultar y cancelar funciones.
- `booking_service.py` lo usará para validar que una compra pertenezca a una
  función válida y activa.
- `seat_repository.py` y `seat_lock_manager.py` trabajarán sobre los asientos
  ligados a esta función.
- `showtime_repository.py` guardará y recuperará esta entidad.

Qué debe resolver esta entidad:
- representar una función de cine,
- mantener datos básicos de programación,
- saber si sigue activa o ya no puede vender boletos,
- ayudar a controlar disponibilidad de asientos,
- evitar cambios de estado inválidos.

Idea importante:
Showtime no debe encargarse de cobrar, hablar con la consola, ni guardar datos
en base de datos. Solo debe contener las reglas del dominio relacionadas con la
función.
"""


from datetime import datetime, timedelta
from typing import Optional

# Se espera usar más adelante el value object Money.
# from cine_boletos_cli.domain.value_objects.money import Money


class Showtime:
    """
    Entidad del dominio que representa una función de cine.
    """

    def __init__(
        self,
        showtime_id,
        movie_id,
        room_id,
        starts_at: datetime,
        duration_minutes: int,
        base_price,
        status,
        ends_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        """
        Inicializa una función de cine.

        Args:
            showtime_id:
                Identificador formal de la función.

            movie_id:
                Identificador de la película que se proyecta.

            room_id:
                Identificador de la sala donde se proyecta.

            starts_at:
                Fecha y hora de inicio de la función.

            duration_minutes:
                Duración de la función en minutos.

            base_price:
                Precio base del boleto para esta función.

            status:
                Estado actual de la función.

            ends_at:
                Fecha y hora de finalización. Si no se entrega, puede calcularse
                a partir de starts_at y duration_minutes.

            created_at:
                Momento en que se creó la función.

            updated_at:
                Momento de la última actualización.
        """
        self.showtime_id = showtime_id
        self.movie_id = movie_id
        self.room_id = room_id
        self.starts_at = starts_at
        self.duration_minutes = duration_minutes
        self.base_price = base_price
        self.status = status
        self.ends_at = ends_at or (starts_at + timedelta(minutes=duration_minutes))
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or self.created_at

    def is_active(self):
        """
        Indica si la función sigue activa y puede usarse para reservas.

        Una función activa es una función que todavía no fue cancelada,
        cerrada o vencida según las reglas del sistema.
        """
        pass

    def has_started(self, now: Optional[datetime] = None):
        """
        Indica si la función ya comenzó.

        Esto sirve para evitar reservar o cancelar en momentos no permitidos.
        """
        pass

    def change_status(self, new_status):
        """
        Cambia el estado de la función.

        Debe validar que la transición sea permitida por las reglas del dominio.
        """
        pass

    def change_price(self, new_price):
        """
        Cambia el precio base de la función.

        Más adelante esto puede usarse para promociones o ajustes de tarifas.
        """
        pass

    def available_seats(self):
        """
        Devuelve la cantidad de asientos disponibles para esta función.

        La lógica real dependerá de los asientos asociados y su estado.
        """
        pass

    def validate_transition(self, new_status):
        """
        Valida si el cambio de estado solicitado es permitido.

        Ejemplos esperados:
        - SCHEDULED -> ACTIVE
        - ACTIVE -> CANCELLED
        - ACTIVE -> FINISHED

        Cambios inválidos deben rechazarse.
        """
        pass