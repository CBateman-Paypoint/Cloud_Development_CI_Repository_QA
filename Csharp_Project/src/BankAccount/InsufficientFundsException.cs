namespace BankAccount;

/// <summary>
/// Thrown when a withdrawal is refused because the account does not hold enough money.
/// </summary>
/// <remarks>
/// A domain-specific exception type lets callers catch exactly this failure instead of
/// catching a general <see cref="InvalidOperationException"/> and guessing at the cause.
/// By convention a custom exception derives from <see cref="Exception"/>, has a name
/// ending in "Exception", and lives in a file named after itself.
/// </remarks>
public class InsufficientFundsException : Exception
{
    /// <summary>The amount the caller asked to withdraw.</summary>
    public decimal RequestedAmount { get; }

    /// <summary>The balance that was actually available at the time of the request.</summary>
    public decimal AvailableBalance { get; }

    public InsufficientFundsException(decimal requestedAmount, decimal availableBalance)
        : base($"Cannot withdraw {requestedAmount:C}: only {availableBalance:C} is available.")
    {
        RequestedAmount = requestedAmount;
        AvailableBalance = availableBalance;
    }
}
