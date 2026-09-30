# Example Repo

A teaching repository for the Cloud Development course. It exists to be poked at:
branched, broken, pushed, and watched in the Actions tab.

Three things live here.

| Folder | What it is for |
|---|---|
| [`Csharp_Project/`](Csharp_Project/) | A reference C# solution with NUnit. Correct layout, correct naming. |
| [`Python_Project/`](Python_Project/) | A reference Python project with both unittest and pytest. |
| [`Documents/`](Documents/) | Scratch files and notes from the git demos: staging, commits, merges, pull requests. |
| [`.github/workflows/`](.github/workflows/) | The CI pipelines that build and test the two projects. |


## The two projects

Both model the same thing, a bank account with a savings variant, ON PURPOSE.
Hold them side by side and the DESIGN is identical while the CONVENTIONS are not.
That contrast is the point of having two.

|  | C# | Python |
|---|---|---|
| Classes | `PascalCase` | `PascalCase` |
| Methods, functions | `PascalCase` | `snake_case` |
| Parameters, locals | `camelCase` | `snake_case` |
| Private field | `_balance` | `_balance` by convention, `__balance` to name-mangle |
| Constants | `PascalCase` | `UPPER_SNAKE_CASE` |
| The exception | `InsufficientFundsException` | `InsufficientFundsError` |
| Test framework | NUnit | unittest AND pytest |

Two of those catch people out:

- **Python classes are `PascalCase`, not `snake_case`.** PEP 8 says so. Delegates told
  "Python is snake_case" tend to over-apply it, and class names are where it shows.
- **Python exceptions end `Error`, C# exceptions end `Exception`.** Same concept, opposite
  house style. Having both repos open makes that obvious in a way a slide does not.

Each project has its own README with the full naming table, the folder rationale, and how
to run it: [C#](Csharp_Project/README.md), [Python](Python_Project/README.md).


## Running them

From the repository root:

```bash
# C#
cd Csharp_Project
dotnet test
# ->  Passed!  Failed: 0, Passed: 15, Skipped: 0, Total: 15

# Python
cd Python_Project
pip install -r requirements.txt
python -m pytest -v            # ->  35 passed
python -m unittest discover -v # ->  Ran 15 tests ... OK
```

**The Python counts differ on purpose and it is not a bug.** pytest collects
`unittest.TestCase` classes as well as its own plain test functions, so it runs BOTH test
files. unittest only understands `TestCase`, so it runs only its own file and ignores the
pytest one. Collection goes one way: pytest can run unittest tests, unittest cannot run
pytest tests.


## The pipelines

| Workflow | Runs |
|---|---|
| `example_csharp_workflow.yml` | restore, build, test, publish the C# project |
| `example_python_workflow.yml` | install, pytest, unittest, then `build.sh` |
| `example_workflow.yml` | the GitHub starter workflow, echoes and nothing else |
| `workflow_variables.md` | a glossary of the keywords, not a workflow |

Two ideas make one repository with two projects work, and both are worth reading in the
workflow files where they are commented in place:

**`defaults.run.working-directory`** - `actions/checkout` puts the WHOLE repository on the
runner, so the working directory is the repo root and `dotnet restore` would find no
project. Setting this once per job moves every `run:` step into the project folder, so the
commands stay exactly as you would type them yourself. It does not affect `uses:` steps,
which is what you want.

**`paths:`** - without it, editing a Python file rebuilds the C# project and vice versa.
The filter also lists the workflow file itself, because after editing a pipeline you
always want it to run.

### Why `workflow_variables` is a `.md` and not a `.yml`

GitHub tries to parse EVERY `.yml` and `.yaml` file in `.github/workflows` as a workflow.
That file is a glossary, all comments, no `on:` and no `jobs:`, so GitHub reported it as an
invalid workflow file. Renaming it to `.md` leaves it exactly where it is useful and stops
GitHub trying to run it.

Worth knowing generally: a file in that folder is either a valid workflow or an error.
There is no "ignore this one" option.


## Notes for anyone pushing this

- The deploy jobs use `environment: production`. That is just a label until you attach a
  required reviewer to it in Settings, at which point the job pauses and waits for a human.
  You cannot tell whether that gate exists by reading the YAML.
- `build.sh` has LF line endings deliberately. A shell script committed with CRLF fails on
  a Linux runner with a `bad interpreter` error that reads like a missing file and is not.
- Build output is ignored via each project's own `.gitignore`: `bin/`, `obj/`, `publish/`,
  `__pycache__/`, `*.egg-info/`, `dist/`. Nothing generated should ever be committed.
- The C# publish step names the project rather than the solution. Publishing the solution
  warns `NETSDK1194` and copies the TEST assembly into the deployment output.
