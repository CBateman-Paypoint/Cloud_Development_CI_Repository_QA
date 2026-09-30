"""bank_account - a tiny banking domain used to demonstrate Python project layout.

The package name is snake_case (in fact all-lowercase, which PEP 8 prefers for
package names). Re-exporting the public names here lets callers write
``from bank_account import Account`` instead of reaching into submodules.
"""

from bank_account.accounts import (
    DEFAULT_INTEREST_RATE,
    MINIMUM_BALANCE,
    Account,
    SavingsAccount,
)
from bank_account.errors import InsufficientFundsError

__all__ = [
    "Account",
    "SavingsAccount",
    "InsufficientFundsError",
    "MINIMUM_BALANCE",
    "DEFAULT_INTEREST_RATE",
]

__version__ = "1.0.0"
