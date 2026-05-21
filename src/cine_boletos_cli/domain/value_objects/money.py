"""
money.py

Value Object para representar valores monetarios dentro del dominio.

Este objeto encapsula montos y monedas utilizando ``Decimal`` para evitar
errores de precisión asociados al uso de ``float`` en operaciones financieras.

Responsibilities
----------------
- representar cantidades monetarias,
- validar compatibilidad de monedas,
- permitir operaciones aritméticas seguras,
- mantener precisión consistente.

Notes
-----
Este objeto no debe:
- acceder a bases de datos,
- procesar pagos,
- manejar lógica de infraestructura,
- ejecutar lógica externa al dominio.
"""

from decimal import Decimal

from cine_boletos_cli.domain.exceptions.domain_errors import CurrencyMismatchError
from cine_boletos_cli.shared.constants import DEFAULT_CURRENCY


class Money:
    """
    Representa un valor monetario dentro del dominio.

    Parameters
    ----------
    amount : str | int | Decimal
        Monto monetario.

    currency : str
        Código de moneda en formato ISO 4217.

    Examples
    --------
    >>> Money("10.50", "USD")
    >>> Money(20, "EUR")
    """
    VALID_TYPES = (str, int, Decimal)

    def __init__(self, amount, currency=DEFAULT_CURRENCY):
        """
        Inicializa un objeto monetario.

        Parameters
        ----------
        amount : str | int | Decimal
            Monto monetario.

        currency : str
            Código de moneda.
        """

        if not isinstance(amount, self.VALID_TYPES):
            raise TypeError(
                "amount debe ser str, int o Decimal."
            )


        self.amount = Decimal(amount)
        self.currency = currency

    def __add__(self, other):
        """
        Suma dos valores monetarios.

        Parameters
        ----------
        other : Money
            Valor monetario a sumar.

        Returns
        -------
        Money
            Nuevo objeto con el resultado de la suma.

        Raises
        ------
        ValueError
            Si las monedas no coinciden.
        """

        self._validate_currency(other)

        return Money(
            amount=self.amount + other.amount,
            currency=self.currency,
        )

    def __sub__(self, other):
        """
        Resta dos valores monetarios.

        Parameters
        ----------
        other : Money
            Valor monetario a restar.

        Returns
        -------
        Money
            Nuevo objeto con el resultado de la resta.

        Raises
        ------
        ValueError
            Si las monedas no coinciden.
        """

        self._validate_currency(other)

        return Money(
            amount=self.amount - other.amount,
            currency=self.currency,
        )

    def __mul__(self, multiplier):
        """
        Multiplica un valor monetario por un factor numérico.

        Parameters
        ----------
        multiplier : int | float | Decimal
            Factor multiplicador.

        Returns
        -------
        Money
            Nuevo objeto con el resultado de la multiplicación.
        """

        return Money(
            amount=self.amount * Decimal(multiplier),
            currency=self.currency,
        )
    
    def __rmul__(self, multiplier):
        """
        Permite multiplicación inversa.

        Examples
        --------
        >>> 3 * Money("10", "USD")
        """

        return self.__mul__(multiplier)

    def __eq__(self, other):
        """
        Compara igualdad entre dos valores monetarios.
        """

        return (
            self.amount == other.amount
            and self.currency == other.currency
        )

    def __lt__(self, other):
        """
        Compara si un valor monetario es menor que otro.

        Raises
        ------
        ValueError
            Si las monedas no coinciden.
        """

        self._validate_currency(other)

        return self.amount < other.amount

    def __le__(self, other):
        """
        Compara si un valor monetario es menor o igual que otro.
        """

        self._validate_currency(other)

        return self.amount <= other.amount

    def __gt__(self, other):
        """
        Compara si un valor monetario es mayor que otro.
        """

        self._validate_currency(other)

        return self.amount > other.amount

    def __ge__(self, other):
        """
        Compara si un valor monetario es mayor o igual que otro.
        """

        self._validate_currency(other)

        return self.amount >= other.amount

    def __repr__(self):
        """
        Retorna representación legible del objeto.
        """

        return f"Money(amount={self.amount}, currency='{self.currency}')"

    def _validate_currency(self, other):
        """
        Valida que dos objetos Money tengan la misma moneda.

        Parameters
        ----------
        other : Money
            Objeto monetario a validar.

        Raises
        ------
        ValueError
            Si las monedas son distintas.
        """

        if self.currency != other.currency:
            raise CurrencyMismatchError(
                "Las monedas de los valores monetarios no coinciden."
                )
