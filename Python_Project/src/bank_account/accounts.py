"""Account types for the bank_account package.

Everything in this module is named deliberately. Read the names as well as the
logic:

* ``accounts``                  - module, snake_case
* ``Account``, ``SavingsAccount`` - classes, PascalCase
* ``MINIMUM_BALANCE``           - module-level constant, UPPER_SNAKE_CASE
* ``deposit``, ``apply_interest`` - methods, snake_case
* ``_validate_amount``          - internal by convention, single leading underscore
* ``__transaction_count``       - name-mangled, double leading underscore
"""

from bank_account.errors import InsufficientFundsError

# Module-level constants: UPPER_SNAKE_CASE.
MINIMUM_BALANCE = 0.0
DEFAULT_INTEREST_RATE = 0.02


class Account:
    """A simple bank account with a balance you can pay into and draw from."""

    def __init__(self, owner_name: str, balance: float = 0.0) -> None:
        if balance < MINIMUM_BALANCE:
            raise ValueError("Opening balance cannot be negative.")
        self.owner_name = owner_name
        self.balance = balance
        # Two leading underscores triggers *name mangling*: outside the class
        # this attribute is reachable only as `_Account__transaction_count`.
        # Use it to avoid clashes in subclasses, not as a security feature.
        self.__transaction_count = 0

    def deposit(self, amount: float) -> float:
        """Pay `amount` into the account and return the new balance."""
        self._validate_amount(amount)
        self.balance += amount
        self.__transaction_count += 1
        return self.balance

    def withdraw(self, amount: float) -> float:
        """Draw `amount` out of the account and return the new balance.

        Raises:
            InsufficientFundsError: If the account does not hold enough.
        """
        self._validate_amount(amount)
        if amount > self.balance:
            raise InsufficientFundsError(requested=amount, available=self.balance)
        self.balance -= amount
        self.__transaction_count += 1
        return self.balance

    @property
    def transaction_count(self) -> int:
        """How many deposits and withdrawals this account has seen."""
        return self.__transaction_count

    @staticmethod
    def _validate_amount(amount: float) -> None:
        """Internal helper. One leading underscore = "not part of the API".

        Nothing stops you calling it from outside; the underscore is a promise
        between developers, not an enforced access modifier like C#'s `private`.
        """
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

    def __repr__(self) -> str:
        return f"{type(self).__name__}(owner_name={self.owner_name!r}, balance={self.balance:.2f})"


class SavingsAccount(Account):
    """An `Account` that also pays interest."""

    def __init__(
        self,
        owner_name: str,
        balance: float = 0.0,
        interest_rate: float = DEFAULT_INTEREST_RATE,
    ) -> None:
        super().__init__(owner_name, balance)
        if interest_rate < 0:
            raise ValueError("Interest rate cannot be negative.")
        self.interest_rate = interest_rate

    def apply_interest(self) -> float:
        """Add one period of interest to the balance and return the interest paid."""
        interest = self.balance * self.interest_rate
        if interest > 0:
            self.deposit(interest)
        return interest
