namespace BankAccount;

/// <summary>
/// A basic bank account: money can be paid in and taken out, and the balance can be read
/// but never assigned from outside the class.
/// </summary>
public class Account
{
    // Private instance fields use _camelCase: a leading underscore then camelCase.
    // The underscore makes it obvious at the point of use that you are touching field
    // state rather than a parameter or a local.
    private readonly string _accountHolder;
    private decimal _balance;

    /// <summary>
    /// Creates an account for the named holder with an optional opening balance.
    /// </summary>
    /// <param name="accountHolder">Name of the person the account belongs to.</param>
    /// <param name="openingBalance">Starting balance; may not be negative.</param>
    public Account(string accountHolder, decimal openingBalance = 0m)
    {
        if (string.IsNullOrWhiteSpace(accountHolder))
        {
            throw new ArgumentException("Account holder must be supplied.", nameof(accountHolder));
        }

        if (openingBalance < 0m)
        {
            throw new ArgumentOutOfRangeException(
                nameof(openingBalance), "Opening balance may not be negative.");
        }

        _accountHolder = accountHolder;
        _balance = openingBalance;
    }

    /// <summary>Name of the account holder.</summary>
    public string AccountHolder => _accountHolder;

    /// <summary>
    /// The current balance. This is the encapsulation point: the field is private and
    /// there is no setter, so the only way to change the balance is through
    /// <see cref="Deposit"/> and <see cref="Withdraw"/>, which enforce the rules.
    /// </summary>
    public decimal Balance => _balance;

    /// <summary>Pays money into the account.</summary>
    /// <param name="amount">A positive amount to add.</param>
    public void Deposit(decimal amount)
    {
        if (amount <= 0m)
        {
            throw new ArgumentOutOfRangeException(
                nameof(amount), "Deposit amount must be greater than zero.");
        }

        _balance += amount;
    }

    /// <summary>Takes money out of the account.</summary>
    /// <param name="amount">A positive amount to remove.</param>
    /// <exception cref="InsufficientFundsException">
    /// Thrown when <paramref name="amount"/> exceeds the current balance.
    /// </exception>
    public void Withdraw(decimal amount)
    {
        if (amount <= 0m)
        {
            throw new ArgumentOutOfRangeException(
                nameof(amount), "Withdrawal amount must be greater than zero.");
        }

        if (amount > _balance)
        {
            throw new InsufficientFundsException(amount, _balance);
        }

        _balance -= amount;
    }

    /// <summary>
    /// A one-line human-readable summary of the account.
    /// </summary>
    /// <remarks>
    /// Marked <c>virtual</c> so a derived type can replace the behaviour. Calling this
    /// through an <see cref="Account"/>-typed variable that actually holds a
    /// <see cref="SavingsAccount"/> runs the derived version: that is polymorphism.
    /// </remarks>
    public virtual string Describe() => $"Account[{_accountHolder}] balance {_balance:C}";
}
