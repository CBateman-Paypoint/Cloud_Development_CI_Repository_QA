namespace BankAccount.Tests;

/// <summary>
/// Tests for <see cref="Account"/>.
/// </summary>
/// <remarks>
/// IMPORTANT NUnit BEHAVIOUR: NUnit creates ONE instance of this class and reuses it for
/// every test in the fixture. It does NOT construct a fresh instance per test the way
/// xUnit.net does. So any state initialised in a field initialiser or a constructor is
/// shared across all the tests here, and a test that mutates it leaks into the next one,
/// which is how you end up with tests that pass alone and fail as a set.
///
/// That is why <see cref="_account"/> is only declared below and is assigned inside the
/// [SetUp] method: [SetUp] runs before EACH test, so every test gets a fresh object.
/// Rule of thumb: declare in a field, construct in [SetUp], never in a field initialiser.
/// </remarks>
[TestFixture]
public class AccountTests
{
    private const string AccountHolder = "John Doe";
    private const decimal OpeningBalance = 100m;

    // Declared here, deliberately NOT initialised here. See the remarks above.
    // "= null!" only tells the nullable analyser that [SetUp] will fill this in.
    private Account _account = null!;

    /// <summary>Runs before every single test in this fixture.</summary>
    [SetUp]
    public void SetUp()
    {
        _account = new Account(AccountHolder, OpeningBalance);
    }

    [Test]
    public void Deposit_PositiveAmount_IncreasesBalance()
    {
        _account.Deposit(25m);

        // Assert.That with the constraint model is current NUnit style.
        // The older Assert.AreEqual(expected, actual) form still exists but is obsolete.
        Assert.That(_account.Balance, Is.EqualTo(125m));
    }

    // [TestCase] runs the same test body once per set of arguments, and each case is
    // reported as its own test. Far better than a loop inside one test, because a failing
    // case is named in the output instead of hiding behind the first failure.
    [TestCase(0)]
    [TestCase(-0.01)]
    [TestCase(-50)]
    public void Deposit_AmountNotGreaterThanZero_ThrowsArgumentOutOfRangeException(decimal amount)
    {
        // The action under test is put in an Action local first. NUnit 4.6 offers
        // several overloads of Assert.That that accept a delegate, so handing it a bare
        // lambda is ambiguous; naming the delegate type resolves it, and it reads better too.
        Action act = () => _account.Deposit(amount);

        Assert.That(act, Throws.TypeOf<ArgumentOutOfRangeException>());
    }

    [Test]
    public void Withdraw_AmountWithinBalance_ReducesBalance()
    {
        _account.Withdraw(40m);

        Assert.That(_account.Balance, Is.EqualTo(60m));
    }

    [Test]
    public void Withdraw_AmountGreaterThanBalance_ThrowsInsufficientFundsException()
    {
        Action act = () => _account.Withdraw(OpeningBalance + 0.01m);

        Assert.That(act, Throws.TypeOf<InsufficientFundsException>());
    }

    [Test]
    public void Withdraw_AmountGreaterThanBalance_LeavesBalanceUnchanged()
    {
        Action act = () => _account.Withdraw(500m);

        // The account must be left exactly as it was when the withdrawal is refused.
        Assert.That(act, Throws.TypeOf<InsufficientFundsException>());
        Assert.That(_account.Balance, Is.EqualTo(OpeningBalance));
    }

    [Test]
    public void Constructor_NegativeOpeningBalance_ThrowsArgumentOutOfRangeException()
    {
        Action act = () => new Account(AccountHolder, -1m);

        Assert.That(act, Throws.TypeOf<ArgumentOutOfRangeException>());
    }

    [Test]
    public void Constructor_BlankAccountHolder_ThrowsArgumentException()
    {
        Action act = () => new Account("   ");

        Assert.That(act, Throws.TypeOf<ArgumentException>());
    }

    [Test]
    public void Describe_BaseAccount_StartsWithAccountAndHolderName()
    {
        // The balance is formatted as currency, which varies by machine culture, so the
        // assertion deliberately checks only the culture-independent part.
        Assert.That(_account.Describe(), Does.StartWith($"Account[{AccountHolder}]"));
    }
}
