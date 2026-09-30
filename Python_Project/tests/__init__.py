"""Test package.

This file is not decoration. It makes ``tests`` a real package, so that
``python -m unittest discover -v`` from the project root can import the test
modules by a proper dotted name (``tests.test_accounts_unittest``) instead of
guessing at a path.
"""
