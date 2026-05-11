"""
Este archivo representará dinero dentro del dominio.

La idea es evitar usar floats directamente para precios y pagos, porque los
floats pueden generar errores de precisión que en sistemas financieros son
muy peligrosos.

Ejemplo:

0.1 + 0.2 != 0.3

En un sistema de boletos eso podría provocar:
- cobros incorrectos,
- totales inconsistentes,
- errores en reembolsos,
- o diferencias en reportes.

Por eso el dinero se modelará como un Value Object formal del dominio y no
como números sueltos.

Este objeto debería encargarse de:
- representar montos monetarios,
- validar moneda,
- permitir operaciones seguras,
- y mantener precisión consistente.

Qué debería tener:
- amount
- currency

Qué debería permitir:
- sumar
- restar
- multiplicar
- comparar

Qué NO debería hacer:
- acceder a base de datos
- procesar pagos
- imprimir tickets
- manejar lógica de negocio externa
"""


from decimal import Decimal


class Money:
    """
    Representa un valor monetario dentro del dominio.
    """

    def __init__(self, amount, currency):
        """
        amount:
            monto monetario.

        currency:
            código de moneda (USD, EUR, etc.).
        """

        # Usar Decimal para evitar errores de precisión con floats.
        self.amount = Decimal(amount)

        self.currency = currency

    def __add__(self, other_money):
        """
        Suma dos cantidades monetarias.

        Antes de sumar debería validarse que ambas monedas sean iguales.

        Ejemplo:
            10 USD + 5 USD = 15 USD

        No debería permitirse:
            10 USD + 5 EUR
        """

        # TODO:
        # - validar moneda
        # - retornar nuevo objeto Money
        pass

    # TODO:
    # - validar monto
    # - validar moneda
    # - implementar resta
    # - implementar multiplicación
    # - implementar comparaciones
    # - evaluar inmutabilidad