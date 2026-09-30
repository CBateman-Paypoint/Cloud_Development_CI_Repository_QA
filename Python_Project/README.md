# Python Project Demo - `bank_account`

Trainer demo material. A deliberately small banking domain, laid out the way a real Python
project should be, with **both** `unittest` and `pytest` tests sitting side by side.

The sibling `Csharp_Project` models the **same** domain. Hold the two up together: the design
is identical, the conventions are not. That contrast is the point.

---

## 1. Folder layout

```
Python_Project/
├── pyproject.toml              # project metadata, build config, pytest config
├── requirements.txt            # pytest + `-e .` (installs this project)
├── .gitignore
├── README.md
├── src/
│   └── bank_account/           # the package - snake_case, lowercase
│       ├── __init__.py         # re-exports the public API
│       ├── accounts.py         # Account, SavingsAccount
│       └── errors.py           # InsufficientFundsError
└── tests/
    ├── __init__.py             # makes `tests` a package (see §5)
    ├── test_accounts_unittest.py
    └── test_accounts_pytest.py
```

### Why `src/` layout?

Without it, the project root is on `sys.path` when you run Python from the root, so
`import bank_account` silently picks up the **folder sitting next to you** rather than the
**installed package**. That hides whole classes of packaging bug: a module you forgot to list,
a data file that never made it into the wheel, a broken `__init__`. Your tests pass locally
and the published package is broken.

Putting the code under `src/` makes that impossible. `src/` is never on `sys.path`, so the only
way to import `bank_account` is to install it. What you test is what you ship.

That is why `requirements.txt` ends with:

```
-e .
```

`-e .` is an **editable install** of this project, read from `pyproject.toml`. One
`pip install -r requirements.txt` therefore installs pytest *and* makes `bank_account`
importable. Verified - after installing, `import bank_account` resolves to:

```
...\Python_Project\src\bank_account\__init__.py
```

---

## 2. Naming conventions (PEP 8)

This is half the reason the demo exists. Python is **not** "snake_case everywhere".

| Thing | Convention | Example in this project |
|---|---|---|
| Package | `lowercase` / `snake_case` | `bank_account` |
| Module (file) | `snake_case` | `accounts.py`, `errors.py` |
| **Class** | **`PascalCase`** | `Account`, `SavingsAccount` |
| **Exception class** | **`PascalCase`**, suffix `...Error` | `InsufficientFundsError` |
| Function / method | `snake_case` | `deposit`, `apply_interest`, `_validate_amount` |
| Variable | `snake_case` | `new_balance`, `interest` |
| Parameter | `snake_case` | `owner_name`, `amount`, `interest_rate` |
| Module-level constant | `UPPER_SNAKE_CASE` | `MINIMUM_BALANCE`, `DEFAULT_INTEREST_RATE` |
| Internal by convention | `_single_leading_underscore` | `_validate_amount` |
| Name-mangled | `__double_leading_underscore` | `__transaction_count` |
| Test module | `test_<module>.py` | `test_accounts_*.py` |
| Test function | `test_<what>_<condition>_<expected>` | `test_withdraw_more_than_balance_raises_insufficient_funds_error` |

### The two that catch people out

**Classes are PascalCase, including exceptions.** Delegates who have been told "Python is
snake_case" write `class savings_account`. PEP 8 does not say that. Classes - all of them,
exceptions included - are PascalCase.

**Exceptions end in `Error`, not `Exception`.** The standard library is `ValueError`,
`KeyError`, `TypeError`, `OSError`. So ours is `InsufficientFundsError`.

> **C# contrast.** The sibling project calls the same class `InsufficientFundsException`,
> because .NET's guideline is the `...Exception` suffix and its base type is `System.Exception`.
> Same concept, opposite suffix. Use each language's convention in that language; do not carry
> `...Exception` into Python or `...Error` into C#.

### `_single` vs `__double`

* `_validate_amount` - one underscore. A **convention only**. Nothing stops you calling it;
  it says "not part of the public API, I may change it". `from module import *` skips it.
* `__transaction_count` - two underscores. Triggers **name mangling**: the interpreter rewrites
  it to `_Account__transaction_count`. It exists to stop a subclass accidentally clobbering a
  base class's attribute. It is **not** a security feature and **not** C#'s `private` - the
  attribute is still reachable, just under its mangled name. `test_name_mangled_attribute_is_reachable_under_mangled_name`
  in the unittest file proves exactly that.

---

## 3. Running it

From the **`Python_Project` root**:

```bash
pip install -r requirements.txt
python -m pytest -v
python -m unittest discover -v
```

These are the same three commands as the CI workflow in
`../example_repo/.github/workflows/example_python_workflow.yml`. Both test commands pass.

---

## 4. The two frameworks

| | `unittest` (`test_accounts_unittest.py`) | `pytest` (`test_accounts_pytest.py`) |
|---|---|---|
| Ships with Python? | Yes, standard library | No, `pip install pytest` |
| Test shape | Methods on a `unittest.TestCase` subclass | Plain module-level functions |
| Shared setup | `setUp()`, runs before every test method | `@pytest.fixture`, requested by parameter name |
| Assertions | `self.assertEqual`, `assertTrue`, `assertAlmostEqual` | bare `assert` |
| Expected exceptions | `with self.assertRaises(...) as context:` | `with pytest.raises(...) as exception_info:` |
| Data-driven tests | Write them out, or `subTest` | `@pytest.mark.parametrize` |
| Naming style | camelCase (`setUp`, `assertEqual`) - a JUnit inheritance, **not** PEP 8 | snake_case throughout |

`pytest.approx` is used where floating-point interest is compared, because `0.1 * 100` is not
exactly `10.0` in binary floating point. The unittest file uses `assertAlmostEqual` for the
same reason.

---

## 5. The teaching point: collection is one-way

**pytest collects and runs `unittest.TestCase` classes. unittest does not collect pytest-style
functions.**

So `python -m pytest` runs **both** files, while `python -m unittest discover` runs **only** the
unittest one. Verified by running, not assumed:

`python -m pytest -v`:

```
collecting ... collected 35 items
...
============================= 35 passed in 0.03s ==============================
```

`python -m unittest discover -v`:

```
----------------------------------------------------------------------
Ran 15 tests in 0.000s

OK
```

**35 vs 15.** The breakdown:

| Source | pytest counts | unittest counts |
|---|---|---|
| `test_accounts_unittest.py` (2 classes, 15 methods) | 15 | 15 |
| `test_accounts_pytest.py` (13 functions, 20 after parametrisation) | 20 | 0 |
| **Total** | **35** | **15** |

Note the 13 → 20: `unittest discover` counts **methods**, but pytest expands each
`@pytest.mark.parametrize` case into its own test, so three parametrised functions become
ten reported tests. That is why the pytest file's 13 written functions show up as 20.

The practical consequence: **if you are migrating a codebase from unittest to pytest, you can
adopt pytest as the runner on day one** and it will keep running every existing `TestCase`
while you write new tests in the pytest style. The reverse does not work.

### Why `discover` does not trip over `src/`

Two things make plain `python -m unittest discover` work from the root:

1. **Nothing under `src/` matches the default pattern.** `discover` looks for `test*.py`;
   `accounts.py` and `errors.py` do not match. And `src/` has no `__init__.py`, so discovery
   does not recurse into it as a package.
2. **`tests/__init__.py` exists.** It makes `tests` a real package, so discovery imports the
   modules as `tests.test_accounts_unittest` rather than guessing at file paths. That is why the
   verbose output shows fully-qualified names like
   `tests.test_accounts_unittest.TestAccount.test_...`.

`unittest discover` *does* import `test_accounts_pytest.py` (it matches `test*.py`), finds no
`TestCase` subclass in it, and contributes zero tests from it. That is harmless, and it is
precisely the asymmetry described above. It does mean pytest must be installed for
`python -m unittest discover` to succeed - which `requirements.txt` guarantees.
