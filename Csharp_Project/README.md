# BankAccount - a reference C# solution layout with NUnit

Trainer demo material. The point of this project is **not** the banking logic, which is
deliberately trivial. The point is what a properly laid out C# solution with a test
project looks like: where files go, what they are called, how namespaces line up with
folders, and how the test project is wired to the code under test.

A Python project in the same course models the **same domain** with the same design. Put
the two side by side: the design is identical, the conventions are completely different.
That contrast is the lesson.

---

## Folder layout

```
Csharp_Project/
  BankAccount.sln                  solution: lists both projects
  global.json                      pins the .NET SDK version
  .gitignore                       keeps build output out of source control
  README.md                        this file
  src/
    BankAccount/
      BankAccount.csproj           the library under test
      Account.cs
      SavingsAccount.cs
      InsufficientFundsException.cs
  tests/
    BankAccount.Tests/
      BankAccount.Tests.csproj     the NUnit test project
      AccountTests.cs
      SavingsAccountTests.cs
```

### Why `src/` and `tests/` are split

* **Shipped code and test code are different things.** Everything under `src/` is
  deployed; nothing under `tests/` ever is. Two top-level folders make that obvious
  at a glance, and it stays obvious as the solution grows.
* **They are separate assemblies.** The tests compile into their own DLL that references
  the library. That forces the tests to use the library the way a real caller would:
  through its public surface. If tests lived inside the same project they could reach
  internal detail and you would stop testing the thing you actually ship.
* **The test project takes dependencies the product must not have.** NUnit and the test
  SDK belong to `BankAccount.Tests` only. The library's `.csproj` has no package
  references at all.
* **It is the conventional shape.** A .NET developer opening this repo knows where to
  look without being told.

### ProjectReference direction

`tests/BankAccount.Tests/BankAccount.Tests.csproj` contains:

```xml
<ProjectReference Include="..\..\src\BankAccount\BankAccount.csproj" />
```

The arrow points **tests → src, and never the reverse.** Production code must not know
that tests exist. If you ever find yourself wanting `src` to reference `tests`, something
has gone wrong in the design - usually a test helper that actually belongs in the
library, or a piece of production code that only exists to make a test pass.

The path is **relative**, so the solution works on any machine and on the CI runner
without anyone editing it.

---

## Naming conventions

Getting these right is half the exercise. Every one of them is applied in this project.

| Element | Convention | Example here |
|---|---|---|
| Namespace | `PascalCase` | `BankAccount`, `BankAccount.Tests` |
| Class | `PascalCase` | `Account`, `SavingsAccount` |
| Method | `PascalCase` | `Deposit`, `ApplyInterest` |
| Property | `PascalCase` | `Balance`, `InterestRate` |
| Public field | `PascalCase` | *(none here - prefer a property)* |
| Enum member | `PascalCase` | *(none here)* |
| Constant | `PascalCase` | `OpeningBalance` in the tests |
| **Private instance field** | **`_camelCase`** (leading underscore) | `_balance`, `_interestRate` |
| Parameter | `camelCase` | `amount`, `accountHolder` |
| Local variable | `camelCase` | `interest`, `emptyAccount` |
| Interface | `PascalCase`, **`I`-prefixed** | *(none here - see below)* |
| File name | `PascalCase`, matches the type | `SavingsAccount.cs` holds `SavingsAccount` |

Points worth saying out loud:

* **The leading underscore on private fields is the one that catches people out.** It is
  not decoration. At the point of use, `_balance` is instantly distinguishable from a
  parameter or a local called `balance`, which is exactly where accidental shadowing
  bugs come from. This is Microsoft's own convention and the .NET runtime repo uses it
  throughout.
* **One public type per file, and the file is named after it.** `Account.cs` contains
  `Account` and nothing else. C# does not force this - the compiler is perfectly happy
  with five classes in one file - but every .NET codebase you will work in expects it,
  and tooling like "go to file" depends on it.
* **The namespace matches the folder path.** `src/BankAccount/Account.cs` declares
  `namespace BankAccount;`. Add a `src/BankAccount/Interest/` folder and its files
  declare `namespace BankAccount.Interest;`. The `<RootNamespace>` in the `.csproj` sets
  the base; folders extend it.
* **Interfaces are `I`-prefixed**: `IAccountStore`, `IInterestCalculator`. There is no
  interface in this project, on purpose - the brief is a naming and structure demo, not
  an architecture demo, and adding a repository or a service layer here would teach
  ceremony rather than convention. The prefix rule is listed because you will meet it
  immediately in real code, and because it is one of the few places .NET deliberately
  keeps Hungarian-style notation.
* **Test project is `<ProjectName>.Tests`**, so `BankAccount.Tests`. Its namespace
  matches: `BankAccount.Tests`.
* **Test class is `<ClassUnderTest>Tests`**, so `AccountTests` tests `Account`. One test
  fixture per class under test.

### Test method naming

```
MethodUnderTest_Scenario_ExpectedResult
```

For example:

```
Withdraw_AmountGreaterThanBalance_ThrowsInsufficientFundsException
ApplyInterest_ZeroBalance_LeavesBalanceUnchanged
```

**This is a widely used convention, not a rule.** Nothing in NUnit or the compiler
enforces it, and you will meet teams using `Should_X_When_Y` or plain prose names. What
matters is that a failure in the CI log tells you what broke without opening the file.
The three-part form does that well, so it is the safest default. Pick one and be
consistent within a codebase.

---

## The domain

Four types, chosen to cover four ideas with no sprawl:

* **`Account`** - **encapsulation.** `_balance` is a private field. `Balance` is a
  read-only property with no setter. The only way to change the balance from outside is
  `Deposit` or `Withdraw`, which enforce the rules. You cannot put the object into an
  invalid state.
* **`SavingsAccount : Account`** - **inheritance.** It keeps every rule it inherits and
  adds `ApplyInterest`. Note that `ApplyInterest` calls the inherited `Deposit` rather
  than touching the balance: the private field is invisible even to a derived class, so
  the deposit rules stay in exactly one place.
* **`Account.Describe()` is `virtual`, `SavingsAccount.Describe()` is `override`** -
  **polymorphism.** `SavingsAccountTests.Describe_CalledThroughBaseType_UsesTheOverride`
  holds a `SavingsAccount` in an `Account`-typed variable and shows the derived version
  running.
* **`InsufficientFundsException`** - a **domain exception.** Callers can catch exactly
  this failure instead of catching something generic and guessing at the cause. It
  carries the requested amount and the available balance so the caller can react, not
  just log.

---

## How to run it

From this folder (`Csharp_Project/`):

```bash
dotnet restore
dotnet build --no-restore
dotnet test --no-build --verbosity normal
dotnet publish -c Release -o ./publish
```

Those are exactly the four commands the CI workflow beside this project runs, in that
order. `--no-restore` and `--no-build` are what make the pipeline fast and honest: each
step uses the output of the previous one rather than silently rebuilding.

Day to day you can just run `dotnet test`, which restores and builds first.

### Target framework and SDK

* **`TargetFramework` is `net8.0`** in both projects, because the CI workflow pins
  `dotnet-version: "8.0.x"`.
* **`global.json` pins the SDK to `9.0.317` with `rollForward: latestFeature`**, matching
  the sibling `unit_test_exercises/csharp` project. This is the distinction people trip
  over: the **SDK** is the toolchain that does the building, the **target framework** is
  what the output runs on. A 9.x SDK builds `net8.0` output perfectly well. Pinning the
  SDK stops a newly installed 10.x SDK from quietly changing build behaviour;
  `latestFeature` still allows patch and feature-band updates within 9.0.

### Real test output

```
Test Run Successful.
Total tests: 15
     Passed: 15
 Total time: 1.1426 Seconds
```

13 test methods; 15 tests, because one `[TestCase]`-driven method contributes three.

---

## NUnit: what the attributes do

| Attribute | What it does |
|---|---|
| `[TestFixture]` | Marks a class as a container of tests. Optional in modern NUnit for a simple non-generic class, but written here because being explicit is clearer for a reader. |
| `[SetUp]` | Runs before **every** test in the fixture. Where you build fresh state. |
| `[TearDown]` | Runs after every test. For releasing things - not used here, nothing needs releasing. |
| `[Test]` | Marks a single test method. |
| `[TestCase(...)]` | Runs the same test body once per argument set, each reported as its own named test. Use it instead of a loop inside one test, so a failing case is named in the output rather than hidden behind the first failure. |

### Assertions: the constraint model

Current NUnit style is `Assert.That(actual, Is.EqualTo(expected))`:

```csharp
Assert.That(_account.Balance, Is.EqualTo(125m));

Action act = () => _account.Withdraw(500m);
Assert.That(act, Throws.TypeOf<InsufficientFundsException>());
```

The older "classic" form, `Assert.AreEqual(expected, actual)`, still exists but is
obsolete and produces build warnings in NUnit 4. It also has the trap that the expected
value comes **first**, the opposite way round from the constraint model. Use
`Assert.That` for everything.

One practical wrinkle shown in the test files: NUnit 4.6 has several `Assert.That`
overloads that accept a delegate, so passing a bare lambda directly is ambiguous and
fails to compile. Assigning it to an `Action` local first resolves it - and gives the
"act" step of arrange/act/assert a name, which reads better anyway. (`TestDelegate`, the
type older examples use here, is deprecated in 4.6 in favour of `Action`.)

### The NUnit behaviour that bites people

**NUnit creates ONE instance of a test class and reuses it for every test in that
class.** It does not construct a fresh instance per test the way xUnit.net does.

So this is a bug waiting to happen:

```csharp
// WRONG: one Account shared by every test in the fixture.
private Account _account = new Account("John Doe", 100m);
```

The first test that deposits or withdraws leaks its change into the next test. You get
the worst kind of failure: tests that pass when run alone and fail when run as a set, or
that depend on execution order.

The fix is to **declare in a field, construct in `[SetUp]`**:

```csharp
private Account _account = null!;

[SetUp]
public void SetUp()
{
    _account = new Account("John Doe", 100m);
}
```

`[SetUp]` runs before each test, so every test gets a clean object. Both test files here
follow this and comment on it.

(`= null!` is not part of the pattern - it only tells the nullable-reference analyser
that `[SetUp]` will assign the field before anything reads it.)

---

## Build output and source control

`.gitignore` covers `bin/`, `obj/` and `publish/`. None of it belongs in a repository:
it is generated, machine-specific, and large. The CI runner produces it from source on
every run, which is the whole point of having a build pipeline.

The checked-in tree is source only - `.cs`, `.csproj`, `.sln`, `global.json`, and this
file.

### One known CI warning

`dotnet publish -c Release -o ./publish` at the solution root emits
`NETSDK1194: The "--output" option isn't supported when building a solution`. That comes
from the pre-existing workflow's command, not from anything in this project. It is a
warning, not an error, and the publish succeeds. `IsPublishable=false` on the test
project keeps the test assembly out of `./publish`, so the published folder contains only
`BankAccount.dll` and its metadata. In a real deployment you would point `publish` at a
specific project rather than the solution.
