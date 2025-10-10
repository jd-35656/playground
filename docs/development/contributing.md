# Contributing

!!! info "Personal Development Reference"
    Quick reference for development setup and workflow

## Development Environment

### 1. Initial Setup

```bash
git clone https://github.com/jd-35656/sealkey.git
cd sealkey
pipx install nox
```

### 2. Create Development Environment

```bash
# Create isolated development environment
nox -s develop-3.13

# Environment location: .nox/develop-3.13/
# Python interpreter: .nox/develop-3-13/bin/python
```

### 3. Activate Virtual Environment

```bash
source .nox/develop-3-13/bin/activate

```

### 4. Deactivate Virtual Environment

```bash
deactivate

```

!!! info "Different Python Versions"
    To use a different Python version, first check available sessions:

    ```bash
    nox -l
    ```

    Output shows available versions:
    ```
    * develop-3.9 -> Set up development environment
    * develop-3.10 -> Set up development environment
    * develop-3.11 -> Set up development environment
    * develop-3.12 -> Set up development environment
    * develop-3.13 -> Set up development environment
    ```

    Then create environment with your preferred version:
    ```bash
    nox -s develop-3.11  # For Python 3.11
    nox -s develop-3.12  # For Python 3.12
    ```

    Interpreter paths for different versions:
    ```
    .nox/develop-3.11/bin/python  # Python 3.11
    .nox/develop-3.12/bin/python  # Python 3.12
    ```

### 3. IDE Setup

=== "VS Code"
    1. Open project folder
    2. Press `Ctrl+Shift+P` → "Python: Select Interpreter"
    3. Choose: `.nox/develop-3-13/bin/python` (or your chosen version)
        ```txt
        .nox/develop-3-13/bin/python
        ```
    4. Install recommended extensions:
        - Python
        - Pylance
        - Ruff

=== "PyCharm"
    1. File → Settings → Project → Python Interpreter
    2. Add Interpreter → Existing Environment
    3. Select: `.nox/develop-3-13/bin/python` (or your chosen version)
        ```txt
        .nox/develop-3-13/bin/python
        ```
    4. Apply and OK

### 4. Verify Setup

!!! success "Test Your Environment"
    ```bash
    # Test the environment
    nox                    # Run all (tests + check)
    nox -s tests
    nox -s lint
    nox -s typecheck
    nox -s check           # Run lint + typecheck
    ```

### 5. Development Workflow

1. **Make changes** to code
2. **Run tests**: `nox -s tests`
3. **Check formatting**: `nox -s lint`
4. **Type check**: `nox -s typecheck` (or run all together: `nox`)
5. **Add changelog** entry if needed
6. **Commit** with conventional commit message

!!! tip "Detailed Testing"
    For comprehensive testing information, see [Testing Guide](testing.md).

## Changelog Entries

!!! note "Required for user-facing changes"
    Add a changelog entry for any changes that affect users.

Create file in `changelog.d/`: `<number>.<type>.md`

**Types:** `added`, `changed`, `deprecated`, `removed`, `fixed`, `security`

**Examples:**

- `123.added.md` → Add JSON validation
- `456.fixed.md` → Fix template loading

## Code Standards

!!! note "Development Standards"
    - **Line length**: 121 characters
    - **Formatting**: `ruff` (auto-fixed by `nox -s lint`)
    - **Type hints**: Required for public APIs
    - **Docstrings**: Google style
    - **Commits**: Conventional commits format

## Key Files

!!! abstract "Important Files"
    - **`noxfile.py`** - All development sessions
    - **`pyproject.toml`** - Project config, dependencies, tools
    - **`.github/workflows/`** - CI/CD automation
    - **`docs/`** - MkDocs documentation
    - **`changelog.d/`** - Changelog fragments

## Common Issues

!!! warning "Troubleshooting"
    - **Tests failing?** → Check `nox -s tests -- -v`
    - **Linting errors?** → Run `nox -s lint` to auto-fix
    - **Type errors?** → Run `nox -s typecheck`
    - **Coverage low?** → Add tests for uncovered lines
    - **CI failing?** → Check GitHub Actions logs
