"""
SeatId representa la identidad formal de un asiento dentro de una función
(showtime).

Existe para evitar usar strings sueltos como "A1", "a1" o "A-1" en distintas
partes del proyecto. Eso reduce errores, hace más claras las comparaciones y
permite que todos los módulos hablen el mismo idioma cuando se refieren a un
asiento.

IMPORTANTE:
el estado de un asiento (AVAILABLE, LOCKED, BOOKED) no pertenece solamente al
asiento físico, sino al asiento dentro de una función específica.

Por ejemplo:
el asiento A-10 puede estar:
- BOOKED para la función de las 6PM,
- pero AVAILABLE para la función de las 9PM.

Por eso este identificador probablemente necesitará incluir el showtime
asociado.

En el futuro este objeto se usará en:
- Seat: para identificar el asiento dentro de una función.
- Booking: para guardar qué asientos fueron comprados.
- Repositories: para buscar y persistir asientos de forma consistente.
- Locking: para bloquear exactamente el asiento correcto.
- Tests: para comparar asientos de manera segura.

La idea es que este archivo quede como la referencia oficial de cómo se
representa un asiento dentro del dominio.
"""


class SeatId:
    """
    Identificador de un asiento asociado a una función específica.

    Reúne la información mínima necesaria para identificar un asiento de forma
    clara y consistente dentro del sistema.
    """

    def __init__(
        self,
        showtime_id: str,
        row: str,
        number: int,
        room_id: str | None = None
    ):
        """
        Crea un identificador de asiento.

        Args:
            showtime_id:
                Función a la que pertenece el asiento.

            row:
                Fila del asiento. Ejemplo: "A", "B", "C".

            number:
                Número del asiento dentro de la fila. Ejemplo: 1, 2, 3.

            room_id:
                Identificador opcional de la sala.
        """

        self.showtime_id = showtime_id
        self.row = row
        self.number = number
        self.room_id = room_id

        # TODO:
        # - validar que showtime_id exista
        # - validar que row no venga vacía
        # - validar que number sea mayor que cero
        # - normalizar la fila si hace falta
        # - decidir si room_id será obligatorio o no

    @classmethod
    def from_string(cls, value: str) -> "SeatId":
        """
        Construye un SeatId a partir de un texto.

        Ejemplo esperado:
            "show_1:A-12"

        TODO del programador:
        - definir formato oficial
        - validar formato
        - parsear correctamente showtime y asiento
        """
        # TODO: implementar parseo
        raise NotImplementedError

    def to_string(self) -> str:
        """
        Devuelve una representación legible del asiento.

        Ejemplo:
            "show_1:A-12"

        Esto servirá para logs, debugging y persistencia.
        """
        # TODO: definir representación oficial
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        """
        Compara dos SeatId por valor y no por identidad.
        """
        # TODO:
        # comparar showtime_id, row, number y room_id
        raise NotImplementedError

    def __repr__(self) -> str:
        """
        Devuelve una representación útil para debugging.
        """
        # TODO: definir representación final
        raise NotImplementedError