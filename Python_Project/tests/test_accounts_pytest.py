"""pytest-style tests for `bank_account.accounts`.

The pytest style, for contrast with `test_accounts_unittest.py`:

* tests are plain module-level functions - no class, no base class
* assertions use the bare `assert` keyword; pytest rewrites it so a failure
  still prints both sides of the comparison
* shared setup is a `@pytest.fixture`, requested by naming it as a parameter
* `@pytest.mark.parametrize` runs one test body over many inputs
* expected exceptions use `pytest.raises`

Everything here is snake_case, because pytest was designed with PEP 8 in mind.
"""

import pytest

from bank_account import Account, InsufficientFundsError, SavingsAccount

OPENING_BALANCE = 100.0


@pytest.fixture
def account() -> Account:
    """A fresh `Account` for each test that asks for one.

    The fixture's NAME is the contract: a test that declares a parameter called
    `account` gets the return value of this function.
    """
    return Account(owner_name="John Doe", balance=OPENING_BALANCE)


@pytest.fixture
def savings_account() -> SavingsAccount:
    """A fresh `SavingsAccount` paying 5%."""
    return SavingsAccount(
        owner_name="Jane Doe", balance=OPENING_BALANCE, interest_rate=0.05
    )


def test_deposit_positive_amount_increases_balance(account: Account) -> None:
    assert account.deposit(25.0) == 125.0
    assert account.balance == 125.0


def test_withdraw_affordable_amount_decreases_balance(account: Account) -> None:
    assert account.withdraw(30.0) == 70.0


def test_withdraw_whole_balance_leaves_zero(account: Account) -> None:
    assert account.withdraw(OPENING_BALANCE) == 0.0


@pytest.mark.parametrize(
    "deposit_amount, expected_balance",
    [
        (1.0, 101.0),
        (50.0, 150.0),
        (0.5, 100.5),
        (900.0, 1000.0),
    ],
)
def test_deposit_various_amounts_gives_expected_balance(
    account: Account, deposit_amount: float, expected_balance: float
) -> None:
    """One test body, four runs. pytest reports each as a separate test."""
    assert account.deposit(deposit_amount) == pytest.approx(expected_balance)


@pytest.mark.parametrize("invalid_amount", [0.0, -1.0, -250.0])
def test_deposit_non_positive_amount_raises_value_error(
    account: Account, invalid_amount: float
) -> None:
    with pytest.raises(ValueError):
        account.deposit(invalid_amount)


def test_withdraw_more_than_balance_raises_insufficient_funds_error(
    account: Account,
) -> None:
    # `pytest.raises` yields an ExceptionInfo; the exception itself is `.value`.
    with pytest.raises(InsufficientFundsError) as exception_info:
        account.withdraw(150.0)
    assert exception_info.value.requested == 150.0
    assert exception_info.value.available == OPENING_BALANCE


def test_insufficient_funds_error_message_mentions_both_amounts(
    account: Account,
) -> None:
    with pytest.raises(InsufficientFundsError, match=r"150\.00"):
        account.withdraw(150.0)


def test_negative_opening_balance_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Account(owner_name="John Doe", balance=-0.01)


def test_transaction_count_after_three_moves_is_three(account: Account) -> None:
    account.deposit(10.0)
    account.deposit(10.0)
    account.withdraw(10.0)
    assert account.transaction_count == 3


def test_apply_interest_adds_expected_amount(savings_account: SavingsAccount) -> None:
    assert savings_account.apply_interest() == pytest.approx(5.0)
    assert savings_account.balance == pytest.approx(105.0)


@pytest.mark.parametrize(
    "interest_rate, expected_interest",
    [
        (0.0, 0.0),
        (0.01, 1.0),
        (0.10, 10.0),
    ],
)
def test_apply_interest_at_various_rates_pays_expected_interest(
    interest_rate: float, expected_interest: float
) -> None:
    savings = SavingsAccount(
        owner_name="Jane Doe", balance=OPENING_BALANCE, interest_rate=interest_rate
    )
    assert savings.apply_interest() == pytest.approx(expected_interest)


def test_savings_account_is_an_account(savings_account: SavingsAccount) -> None:
    assert isinstance(savings_account, Account)


def test_repr_shows_class_name_and_balance(savings_account: SavingsAccount) -> None:
    assert repr(savings_account).startswith("SavingsAccount(")
    assert "100.00" in repr(savings_account)
