"""unittest-style tests for `bank_account.accounts`.

The unittest style, for contrast with `test_accounts_pytest.py`:

* tests live in a class deriving from `unittest.TestCase` (PascalCase, and it
  must start with `Test` for discovery to find it)
* shared setup goes in `setUp`, which runs before EVERY test method
* assertions are methods: `assertEqual`, `assertTrue`, `assertAlmostEqual`
* expected exceptions use `assertRaises` as a context manager

Note the camelCase on `setUp` and `assertEqual`. That is not PEP 8; it is a
historical wart inherited from JUnit, which unittest was ported from. Your own
code should be snake_case.
"""

import unittest

from bank_account import Account, InsufficientFundsError, SavingsAccount

# Module-level constant in a test module: still UPPER_SNAKE_CASE.
OPENING_BALANCE = 100.0


class TestAccount(unittest.TestCase):
    """Behaviour of the base `Account` class."""

    def setUp(self) -> None:
        """Runs before each test method, giving every test a fresh account."""
        self.account = Account(owner_name="John Doe", balance=OPENING_BALANCE)

    def test_deposit_positive_amount_increases_balance(self) -> None:
        new_balance = self.account.deposit(50.0)
        self.assertEqual(new_balance, 150.0)
        self.assertEqual(self.account.balance, 150.0)

    def test_deposit_zero_amount_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.account.deposit(0.0)

    def test_deposit_negative_amount_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.account.deposit(-10.0)

    def test_withdraw_affordable_amount_decreases_balance(self) -> None:
        new_balance = self.account.withdraw(40.0)
        self.assertEqual(new_balance, 60.0)

    def test_withdraw_whole_balance_leaves_zero(self) -> None:
        self.assertEqual(self.account.withdraw(OPENING_BALANCE), 0.0)

    def test_withdraw_more_than_balance_raises_insufficient_funds_error(self) -> None:
        # assertRaises as a context manager also hands back the exception,
        # so the test can inspect it.
        with self.assertRaises(InsufficientFundsError) as context:
            self.account.withdraw(500.0)
        self.assertEqual(context.exception.requested, 500.0)
        self.assertEqual(context.exception.available, OPENING_BALANCE)

    def test_withdraw_failure_leaves_balance_unchanged(self) -> None:
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(500.0)
        self.assertEqual(self.account.balance, OPENING_BALANCE)

    def test_negative_opening_balance_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            Account(owner_name="John Doe", balance=-1.0)

    def test_transaction_count_new_account_is_zero(self) -> None:
        self.assertEqual(self.account.transaction_count, 0)

    def test_transaction_count_after_two_moves_is_two(self) -> None:
        self.account.deposit(10.0)
        self.account.withdraw(5.0)
        self.assertEqual(self.account.transaction_count, 2)

    def test_name_mangled_attribute_is_reachable_under_mangled_name(self) -> None:
        # Demonstrates what `__transaction_count` actually does: the attribute
        # is renamed, not hidden.
        self.assertTrue(hasattr(self.account, "_Account__transaction_count"))
        self.assertFalse(hasattr(self.account, "__transaction_count"))


class TestSavingsAccount(unittest.TestCase):
    """Behaviour added by the `SavingsAccount` subclass."""

    def setUp(self) -> None:
        self.savings = SavingsAccount(
            owner_name="Jane Doe", balance=OPENING_BALANCE, interest_rate=0.05
        )

    def test_apply_interest_adds_expected_amount_to_balance(self) -> None:
        interest = self.savings.apply_interest()
        self.assertAlmostEqual(interest, 5.0)
        self.assertAlmostEqual(self.savings.balance, 105.0)

    def test_apply_interest_on_empty_account_pays_nothing(self) -> None:
        empty = SavingsAccount(owner_name="John Doe", balance=0.0)
        self.assertEqual(empty.apply_interest(), 0.0)
        self.assertEqual(empty.balance, 0.0)

    def test_savings_account_inherits_withdraw_behaviour(self) -> None:
        with self.assertRaises(InsufficientFundsError):
            self.savings.withdraw(1_000.0)

    def test_negative_interest_rate_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            SavingsAccount(owner_name="Jane Doe", interest_rate=-0.01)


if __name__ == "__main__":
    unittest.main()
