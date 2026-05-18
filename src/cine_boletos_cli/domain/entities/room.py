"""
Este archivo define la entidad Room.

¿Por qué existe?
Porque el sistema necesita representar las salas físicas del cine. Una función
(Showtime) ocurre dentro de una sala específica, y esa sala define:
- capacidad,
- distribución de asientos,
- nombre,
- y configuración física.

¿Cómo se usará más adelante?
- `showtime.py` utilizará Room para saber dónde ocurre una función.
- `generate_seat_map()` ayudará a construir los asientos iniciales de una sala.
- `seat.py` representará los asientos concretos derivados de esta estructura.
- futuros servicios administrativos permitirán crear, editar o desactivar salas.

Qué debe resolver esta entidad:
- representar una sala física,
- mantener información estructural,
- calcular capacidad,
- validar configuraciones,
- generar una estructura inicial de asientos.

Importante:
Room NO debe encargarse de:
- pagos,
- reservas,
- locking,
- persistencia,
- ni interacción con consola.

Solo representa reglas y datos físicos de una sala.
"""


from datetime import datetime
from typing import Optional


class Room:
    """
    Entidad de dominio que representa una sala de cine.
    """

    def __init__(
        self,
        room_id,
        name,
        total_rows,
        seats_per_row,
        status,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        """
        Inicializa una sala de cine.

        Args:
            room_id:
                Identificador formal de la sala.

            name:
                Nombre visible de la sala.

                Ejemplos:
                - Sala 1
                - IMAX
                - VIP Norte

            total_rows:
                Cantidad de filas físicas.

            seats_per_row:
                Cantidad de asientos por fila.

            status:
                Estado actual de la sala.

            created_at:
                Fecha de creación.

            updated_at:
                Última actualización.
        """
        self.room_id = room_id
        self.name = name
        self.total_rows = total_rows
        self.seats_per_row = seats_per_row
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or self.created_at

    def capacity(self):
        """
        Devuelve la capacidad total de la sala.

        La capacidad normalmente será:

            filas * asientos_por_fila

        Ejemplo:
            10 filas * 12 asientos = 120 asientos
        """
        pass

    def is_active(self):
        """
        Indica si la sala puede utilizarse para crear funciones.

        Una sala inactiva no debería aceptar nuevos showtimes.
        """
        pass

    def generate_seat_map(self):
        """
        Genera una estructura inicial de asientos para la sala.

        Idea importante:
        Room conoce la estructura física de la sala, por eso puede ayudar
        a construir el mapa base de asientos.

        Más adelante este método podría:
        - crear filas,
        - generar SeatId,
        - producir estructuras como:
            A1, A2, A3...
            B1, B2, B3...

        Este método NO debe guardar nada en base de datos.
        Solo generar la representación lógica inicial.
        """
        pass

    def rename(self, new_name):
        """
        Cambia el nombre visible de la sala.

        Debe validar:
        - nombres vacíos,
        - longitud inválida,
        - posibles conflictos de negocio.
        """
        pass

    def validate_configuration(self):
        """
        Valida que la configuración física de la sala sea válida.

        Ejemplos:
        - filas mayores a cero,
        - asientos mayores a cero,
        - límites razonables de capacidad.

        Debe impedir configuraciones absurdas o inválidas.
        """
        pass