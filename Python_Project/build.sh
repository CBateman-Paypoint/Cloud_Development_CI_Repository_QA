#!/usr/bin/env bash
#
# Build script for the Python project.
#
# The CI workflow runs this in its deploy job, after the tests have passed.
# It is deliberately dependency free: nothing here needs installing beyond
# what is already in requirements.txt, so it behaves the same on the runner
# as it does on your machine.

set -euo pipefail
# set -e  stop at the first command that fails
# set -u  treat an unset variable as an error, so a typo is caught
# set -o pipefail  a pipeline fails if ANY command in it fails, not just the
#         last one. Without this, "false | true" succeeds, which is rarely
#         what you meant.

echo "==> Verifying the package imports"
python -c "import bank_account; print('   ', bank_account.__name__, bank_account.__file__)"

echo "==> Running the unittest suite as a final gate"
python -m unittest discover

echo "==> Packaging"
rm -rf dist
mkdir -p dist
tar -czf dist/bank_account.tar.gz -C src bank_account
#     -c create, -z gzip, -f the filename that follows
#     -C src  change into src FIRST, so the archive holds bank_account/... and
#             not src/bank_account/..., which is what you want when unpacking.

echo "==> Built dist/bank_account.tar.gz"
ls -lh dist/bank_account.tar.gz
