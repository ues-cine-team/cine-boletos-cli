"""
seat_id.py

Value Object que representa la identidad formal de un asiento dentro de una
función específica.

Este objeto evita el uso de strings sueltos para identificar asientos y
proporciona una representación consistente dentro del dominio.

Responsibilities
----------------
- identificar un asiento dentro de una función,
- validar información básica del identificador,
- normalizar datos de entrada,
- permitir comparaciones seguras por valor.

Notes
-----
El estado de un asiento pertenece al contexto de una función específica
(showtime) y no únicamente al asiento físico.
"""


from cine_boletos_cli.domain.exceptions.domain_errors import InvalidSeatIdentifierError


class SeatId:
    """
    Identificador único de un asiento dentro de una función.

    Parameters
    ----------
    showtime_id : str
        Identificador de la función.

    row : str
        Fila del asiento.

    number : int
        Número del asiento.

    room_id : str | None, optional
        Identificador opcional de la sala.
    """

    def __init__(
        self,
        showtime_id: str,
        row: str,
        number: int,
        room_id: str | None = None,
    ):
        """
        Inicializa un identificador de asiento.

        Parameters
        ----------
        showtime_id : str
            Identificador de la función.

        row : str
            Fila del asiento.

        number : int
            Número del asiento.

        room_id : str | None, optional
            Identificador de la sala.
        """

        if not showtime_id:
            raise InvalidSeatIdentifierError(
                "showtime_id no puede estar vacío."
            )

        if not row:
            raise InvalidSeatIdentifierError("row no puede estar vacío.")

        if number <= 0:
            raise InvalidSeatIdentifierError("seat number debe ser mayor que cero.")

        self.showtime_id = showtime_id
        self.row = row.strip().upper()
        self.number = number
        self.room_id = room_id

    @classmethod
    def from_string(cls, value: str) -> "SeatId":
        """
        Construye un SeatId desde un string.

        Expected format
        ---------------
        showtime_id:ROW-NUMBER

        Example
        -------
        show_1:A-12

        Parameters
        ----------
        value : str
            Representación textual del asiento.

        Returns
        -------
        SeatId
            Nueva instancia de SeatId.

        Raises
        ------
        ValueError
            Si el formato es inválido.
        """

        try:
            showtime_id, seat = value.split(":")
            row, number = seat.split("-")

            return cls(
                showtime_id=showtime_id,
                row=row,
                number=int(number),
            )

        except (ValueError, TypeError):
            raise InvalidSeatIdentifierError(
                "Formato del identificador inválido."
            )

    def to_string(self) -> str:
        """
        Retorna una representación textual del asiento.

        Returns
        -------
        str
            Representación oficial del identificador.
        """

        return f"{self.showtime_id}:{self.row}-{self.number}"

    def __eq__(self, other: object) -> bool:
        """
        Compara dos SeatId por valor.

        Parameters
        ----------
        other : object
            Objeto a comparar.

        Returns
        -------
        bool
            True si ambos identificadores son equivalentes.
        """

        if not isinstance(other, SeatId):
            return False

        return (
            self.showtime_id == other.showtime_id
            and self.row == other.row
            and self.number == other.number
            and self.room_id == other.room_id
        )

    def __repr__(self) -> str:
        """
        Retorna representación útil para debugging.

        Returns
        -------
        str
            Representación del objeto.
        """

        return (
            "SeatId("
            f"showtime_id='{self.showtime_id}', "
            f"row='{self.row}', "
            f"number={self.number}, "
            f"room_id='{self.room_id}'"
            ")"
        )