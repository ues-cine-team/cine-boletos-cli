"""
Este archivo define el contrato del repositorio de asientos.

¿Por qué existe?
Porque la entidad Seat no debe saber cómo se guarda ni cómo se lee desde una
base de datos. Esa responsabilidad se separa aquí para mantener el dominio
limpio y evitar mezclar reglas de negocio con detalles técnicos.

¿Cómo se usará más adelante?
- `seat_service.py` usará este repositorio para consultar y actualizar asientos.
- `booking_service.py` lo usará para validar disponibilidad y confirmar cambios.
- `seat_lock_manager.py` podrá apoyarse en los estados persistidos de los asientos.
- `lock_expiry_worker.py` lo usará para liberar asientos que ya vencieron.
- Más adelante este archivo tendrá una implementación concreta con la tecnología
  de persistencia elegida.

Qué debe resolver este repositorio:
- buscar asientos,
- guardar cambios de estado,
- listar asientos por función,
- consultar disponibilidad,
- recuperar asientos bloqueados, comprados o libres.

Importante:
Este archivo NO debe contener reglas de negocio.
No debe decidir si un asiento puede bloquearse o comprarse.
Eso pertenece a la entidad Seat y a los servicios del dominio.
El repositorio solo guarda, recupera y actualiza datos.
"""


class SeatRepository:
    """
    Contrato del repositorio de asientos.

    Más adelante aquí irá la implementación real de persistencia.
    """

    def save(self, seat):
        """
        Guarda o actualiza un asiento.

        Debe usarse cuando:
        - se bloquea un asiento,
        - se libera,
        - se confirma la compra,
        - o se corrige su estado.

        Args:
            seat:
                Entidad Seat ya validada por el dominio.

        Returns:
            Seat: el asiento persistido.
        """
        pass

    def get_by_id(self, seat_id):
        """
        Busca un asiento por su identidad.

        Args:
            seat_id:
                Identificador del asiento.

        Returns:
            Seat | None: el asiento encontrado o None si no existe.
        """
        pass

    def list_by_showtime(self, showtime_id):
        """
        Devuelve todos los asientos de una función.

        Args:
            showtime_id:
                Identificador de la función.

        Returns:
            list[Seat]: lista de asientos asociados a la función.
        """
        pass

    def list_available(self, showtime_id):
        """
        Devuelve los asientos disponibles de una función.

        Args:
            showtime_id:
                Identificador de la función.

        Returns:
            list[Seat]: asientos libres para reservar.
        """
        pass

    def list_locked(self, showtime_id):
        """
        Devuelve los asientos bloqueados de una función.

        Args:
            showtime_id:
                Identificador de la función.

        Returns:
            list[Seat]: asientos actualmente bloqueados.
        """
        pass

    def list_booked(self, showtime_id):
        """
        Devuelve los asientos ya comprados de una función.

        Args:
            showtime_id:
                Identificador de la función.

        Returns:
            list[Seat]: asientos confirmados como vendidos.
        """
        pass

    def delete(self, seat_id):
        """
        Elimina un asiento o lo marca como inactivo, según la estrategia del sistema.

        Args:
            seat_id:
                Identificador del asiento.

        Returns:
            None
        """
        pass