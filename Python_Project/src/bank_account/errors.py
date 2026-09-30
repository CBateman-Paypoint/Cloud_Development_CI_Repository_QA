"""Custom exception types for the bank_account package.

NAMING NOTE
-----------
The module name is snake_case (``errors``), but the exception class inside it is
PascalCase (``InsufficientFundsError``). PEP 8 asks for PascalCase on every
class, and exceptions are just classes.

The suffix is ``...Error``, not ``...Exception``. That is the Python convention
(see ``ValueError``, ``KeyError``, ``OSError`` in the standard library). The
sibling C# project names the same idea ``InsufficientFundsException``, because
that is the .NET convention. Same design, different house style.
"""


class InsufficientFundsError(Exception):
    """Raised when a withdrawal would take an account below its minimum balance.

    Args:
        requested: The amount the caller tried to withdraw.
        available: The amount that was actually available to withdraw.
    """

    def __init__(self, requested: float, available: float) -> None:
        # `requested` and `available` are parameters, so snake_case.
        self.requested = requested
        self.available = available
        super().__init__(
            f"Cannot withdraw {requested:.2f}: only {available:.2f} available."
        )
