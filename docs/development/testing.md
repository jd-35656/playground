# Testing

## Available Sessions

!!! info "List Available Sessions"
    ```bash
    nox -l
    ```

    Output:
    ```
    Sessions defined in /path/to/project/noxfile.py:

    - develop-3.8          # Create development environment
    - develop-3.9          # Create development environment
    - develop-3.10         # Create development environment
    - develop-3.11         # Create development environment
    - develop-3.12         # Create development environment
    - develop-3.13         # Create development environment
    * tests-3.8            # Run tests with coverage
    * tests-3.9            # Run tests with coverage
    * tests-3.10           # Run tests with coverage
    * tests-3.11           # Run tests with coverage
    * tests-3.12           # Run tests with coverage
    * tests-3.13           # Run tests with coverage
    - lint                 # Code formatting and linting
    - typecheck            # Type checking with mypy
    * check                # Run lint + typecheck
    - build                # Build package distributions
    - changelog            # Generate changelog from fragments
    - docs_serve           # Serve documentation locally
    - docs_deploy          # Deploy documentation to GitHub Pages

    sessions marked with * are selected, sessions marked with - are skipped.
    ```

## Running Tests

=== "Basic Commands"
    ```bash
    # Run tests on all Python versions
    nox -s tests

    # Run tests on specific Python version
    nox -s tests-3.13

    # Run default sessions (tests + check)
    nox
    ```

=== "Custom Arguments"
    ```bash
    # Verbose output
    nox -s tests-3.13 -- -v

    # Run specific test pattern
    nox -s tests-3.13 -- -k test_version

    # Run specific test file
    nox -s tests-3.13 -- tests/test_cli.py

    # Run with short traceback
    nox -s tests-3.13 -- --tb=short

    # Run with coverage report
    nox -s tests-3.13 -- --cov-report=html

    # Multiple arguments
    nox -s tests-3.13 -- -v -k test_cli --tb=short
    ```

!!! tip "Common pytest Arguments"
    ```bash
    -v, --verbose           # Verbose output
    -s                      # Don't capture output (print statements)
    -x, --exitfirst        # Stop on first failure
    -k EXPRESSION          # Run tests matching expression
    --tb=short             # Short traceback format
    --tb=long              # Long traceback format
    --tb=no                # No traceback
    --lf, --last-failed    # Run only last failed tests
    --ff, --failed-first   # Run failed tests first
    ```

## Code Quality Checks

=== "Linting"
    ```bash
    # Run all linting checks
    nox -s lint

    # This runs pre-commit hooks including:
    # - ruff (formatting and linting)
    # - mypy (type checking)
    # - codespell (spell checking)
    ```

=== "Type Checking"
    ```bash
    # Run mypy type checking
    nox -s typecheck

    # With specific arguments
    nox -s typecheck -- --strict
    nox -s typecheck -- src/path/to/typecheck/
    ```

=== "Combined"
    ```bash
    # Run both lint and typecheck
    nox -s check

    # Run tests and checks together
    nox
    ```

## Coverage Reports

!!! success "Coverage Information"
    Tests automatically generate coverage reports:

    - **Terminal**: Shows percentage and missing lines
    - **Minimum**: 90% required
    - **Current**: 100% achieved

## Documentation Development

!!! note "Documentation Commands"
    ```bash
    # Serve docs locally with live reload
    nox -s docs_serve

    # Access at: http://127.0.0.1:8000
    # Auto-reloads when you edit .md files
    ```

## Requirements

!!! abstract "Testing Requirements"
    - **Python**: 3.8+ (tests run on 3.8-3.13)
    - **Coverage**: 90% minimum
    - **Test structure**: `test_*.py` files with `Test*` classes
