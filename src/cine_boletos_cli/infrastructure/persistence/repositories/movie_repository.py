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
    Contrato del repositorio de películas.

    Más adelante aquí irá la implementación real de persistencia.
    """

    def save(self, movie):
        """
        Guarda o actualiza una película.

        Debe usarse cuando:
        - se crea una nueva película,
        - se cambia el título,
        - se actualiza la descripción,
        - se archiva,
        - o se corrige cualquier dato persistido.

        Args:
            movie:
                Entidad Movie ya validada por el dominio.

        Returns:
            Movie: la película persistida.
        """
        pass

    def get_by_id(self, movie_id):
        """
        Busca una película por su identificador.

        Args:
            movie_id:
                Identificador formal de la película.

        Returns:
            Movie | None: la película encontrada o None si no existe.
        """
        pass

    def list_all(self):
        """
        Devuelve todas las películas del catálogo.

        Returns:
            list[Movie]: lista completa de películas.
        """
        pass

    def list_active(self):
        """
        Devuelve solo las películas activas.

        Esto permitirá más adelante:
        - mostrar catálogo disponible,
        - crear funciones sobre películas válidas,
        - construir cartelera pública.

        Returns:
            list[Movie]: películas activas.
        """
        pass

    def search_by_title(self, title):
        """
        Busca películas por título o coincidencia parcial.

        Args:
            title:
                Texto de búsqueda.

        Returns:
            list[Movie]: películas que coinciden con la búsqueda.
        """
        pass

    def delete(self, movie_id):
        """
        Elimina una película o la marca como inactiva,
        según la estrategia del sistema.

        Args:
            movie_id:
                Identificador de la película.

        Returns:
            None
        """
        pass