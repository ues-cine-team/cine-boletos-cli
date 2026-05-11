"""
Este archivo define el contrato del repositorio de funciones (Showtime).

¿Por qué existe?
Porque la entidad Showtime no debe saber cómo se guarda ni cómo se consulta
desde una base de datos. Esa responsabilidad se separa aquí para mantener el
dominio limpio y evitar mezclar reglas de negocio con detalles técnicos.

¿Cómo se usará más adelante?
- `showtime_service.py` usará este repositorio para crear y administrar funciones.
- `purchase_tickets.py` consultará funciones activas antes de permitir compras.
- `booking_service.py` verificará disponibilidad y estado de una función.
- futuros módulos administrativos podrían usarlo para programación y reportes.

Qué debe resolver este repositorio:
- guardar funciones,
- recuperar funciones por ID,
- buscar funciones activas,
- listar funciones por película o sala,
- consultar funciones futuras,
- actualizar cambios de estado u horarios.

Importante:
Este archivo NO debe decidir:
- si una función puede cancelarse,
- si ya comenzó,
- si todavía acepta reservas,
- ni si sus cambios son válidos.

Eso pertenece a la entidad Showtime y a los servicios del dominio.
El repositorio solo guarda, recupera y actualiza datos.
"""


class ShowtimeRepository:
    """
    Contrato del repositorio de funciones.

    Más adelante aquí irá la implementación real de persistencia.
    """

    def save(self, showtime):
        """
        Guarda o actualiza una función.

        Debe usarse cuando:
        - se crea una nueva función,
        - cambia el estado,
        - se modifica el horario,
        - se cambia el precio,
        - o se actualiza cualquier dato persistido.

        Args:
            showtime:
                Entidad Showtime ya validada por el dominio.

        Returns:
            Showtime: la función persistida.
        """
        pass

    def get_by_id(self, showtime_id):
        """
        Busca una función por su identificador.

        Args:
            showtime_id:
                Identificador formal de la función.

        Returns:
            Showtime | None: la función encontrada o None si no existe.
        """
        pass

    def list_active(self):
        """
        Devuelve todas las funciones activas.

        Esto permitirá más adelante:
        - mostrar cartelera,
        - habilitar compras,
        - construir dashboards.

        Returns:
            list[Showtime]: funciones activas.
        """
        pass

    def list_by_movie(self, movie_id):
        """
        Devuelve todas las funciones asociadas a una película.

        Args:
            movie_id:
                Identificador de la película.

        Returns:
            list[Showtime]: funciones de la película.
        """
        pass

    def list_by_room(self, room_id):
        """
        Devuelve todas las funciones asociadas a una sala.

        Args:
            room_id:
                Identificador de la sala.

        Returns:
            list[Showtime]: funciones de la sala.
        """
        pass

    def list_future_showtimes(self):
        """
        Devuelve funciones futuras que todavía no comienzan.

        Más adelante esto servirá para:
        - programación,
        - reservas,
        - consultas de cartelera.

        Returns:
            list[Showtime]: funciones futuras.
        """
        pass

    def delete(self, showtime_id):
        """
        Elimina una función o la marca como inactiva,
        según la estrategia del sistema.

        Args:
            showtime_id:
                Identificador de la función.

        Returns:
            None
        """
        pass