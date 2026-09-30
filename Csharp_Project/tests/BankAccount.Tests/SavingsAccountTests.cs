namespace BankAccount.Tests;

/// <summary>
/// Tests for <see cref="SavingsAccount"/>.
/// </summary>
/// <remarks>
/// As in <see cref="AccountTests"/>, the fixture instance is shared across every test in
/// this class, so the account under test is built in [SetUp] and not in a field
/// initialiser. See the remarks on <see cref="AccountTests"/> for the full explanation.
/// </remarks>
[TestFixture]
public class SavingsAccountTests
{
    private const string AccountHolder = "Jane Doe";
    private const decimal InterestRate = 0.05m;
    private const decimal OpeningBalance = 1000m;

    private SavingsAccount _savingsAccount = null!;

    [SetUp]
    public void SetUp()
    {
        _savingsAccount = new SavingsAccount(AccountHolder, InterestRate, OpeningBalance);
    }

    [Test]
    public void ApplyInterest_PositiveBalance_AddsInterestToBalance()
    {
        _savingsAccount.ApplyInterest();

        Assert.That(_savingsAccount.Balance, Is.EqualTo(1050m));
    }

    [Test]
    public void ApplyInterest_PositiveBalance_ReturnsInterestPaid()
    {
        decimal interest = _savingsAccount.ApplyInterest();

        Assert.That(interest, Is.EqualTo(50m));
    }

    [Test]
    public void ApplyInterest_ZeroBalance_LeavesBalanceUnchanged()
    {
        SavingsAccount emptyAccount = new SavingsAccount(AccountHolder, InterestRate);

        decimal interest = emptyAccount.ApplyInterest();

        Assert.That(interest, Is.EqualTo(0m));
        Assert.That(emptyAccount.Balance, Is.EqualTo(0m));
    }

    [Test]
    public void Withdraw_InheritedFromAccount_StillEnforcesTheBalance()
    {
        // Inherited behaviour is worth one test: the derived type must not have loosened
        // the rule it inherited.
        Action act = () => _savingsAccount.Withdraw(OpeningBalance + 1m);

        Assert.That(act, Throws.TypeOf<InsufficientFundsException>());
    }

    [Test]
    public void Describe_CalledThroughBaseType_UsesTheOverride()
    {
        // The variable is typed as the base class but holds a SavingsAccount, so the
        // overridden Describe runs. That is polymorphism in one line.
        Account account = _savingsAccount;

        Assert.That(account.Describe(), Does.StartWith($"Savings[{AccountHolder}]"));
    }
}
