namespace BankAccount;

/// <summary>
/// An <see cref="Account"/> that also pays interest.
/// </summary>
/// <remarks>
/// Inheritance is appropriate here because a savings account genuinely is an account:
/// it keeps every rule the base class enforces and only adds one behaviour.
/// </remarks>
public class SavingsAccount : Account
{
    private readonly decimal _interestRate;

    /// <summary>
    /// Creates a savings account.
    /// </summary>
    /// <param name="accountHolder">Name of the person the account belongs to.</param>
    /// <param name="interestRate">Annual rate as a fraction, so 0.05m means 5%.</param>
    /// <param name="openingBalance">Starting balance; may not be negative.</param>
    public SavingsAccount(string accountHolder, decimal interestRate, decimal openingBalance = 0m)
        : base(accountHolder, openingBalance)
    {
        if (interestRate < 0m)
        {
            throw new ArgumentOutOfRangeException(
                nameof(interestRate), "Interest rate may not be negative.");
        }

        _interestRate = interestRate;
    }

    /// <summary>The annual interest rate as a fraction, so 0.05m means 5%.</summary>
    public decimal InterestRate => _interestRate;

    /// <summary>
    /// Adds one period of interest to the balance and returns the interest paid.
    /// </summary>
    /// <remarks>
    /// Note that this goes through the inherited <see cref="Account.Deposit"/> rather
    /// than touching the balance directly. The balance field is private to
    /// <see cref="Account"/>, so even a derived class has to use the public behaviour,
    /// which keeps the deposit rules in exactly one place.
    /// </remarks>
    public decimal ApplyInterest()
    {
        decimal interest = decimal.Round(Balance * _interestRate, 2);

        if (interest > 0m)
        {
            Deposit(interest);
        }

        return interest;
    }

    /// <inheritdoc />
    public override string Describe() =>
        $"Savings[{AccountHolder}] balance {Balance:C} at {_interestRate:P2}";
}
