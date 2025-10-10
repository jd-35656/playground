# Installation

!!! tip "Recommended Installation Method"
    [pipx](https://pypa.github.io/pipx/) is the recommended way to install sealkey. It installs the package in an isolated environment while making the command globally available.

## Using pipx

### Install pipx (if you don't have it)

=== "macOS"
    ```bash
    brew install pipx
    pipx ensurepath
    ```

=== "Ubuntu/Debian"
    ```bash
    sudo apt update
    sudo apt install pipx
    pipx ensurepath
    sudo pipx ensurepath --global # optional to allow pipx actions with --global argument
    ```

=== "Windows"
    ```powershell
    # Using scoop
    scoop install pipx

    # Or using pip
    python -m pip install --user pipx
    python -m pipx ensurepath
    ```

=== "Other Linux"
    ```bash
    python -m pip install --user pipx
    python -m pipx ensurepath
    ```

### Install sealkey with pipx

!!! success "Install Command"
    ```bash
    pipx install sealkey
    ```

### Verify installation

!!! note "Verify Installation"
    ```bash
    sealkey --version
    ```

## Alternative: Using pip

!!! info "Alternative Method"
    If you prefer to use pip directly:

    ```bash
    pip install sealkey
    ```

!!! warning "Virtual Environment Recommended"
    When using pip, it's recommended to install in a virtual environment to avoid conflicts:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install sealkey
    ```

## Upgrading

=== "pipx"
    ```bash
    pipx upgrade sealkey
    ```

=== "pip"
    ```bash
    pip install --upgrade sealkey
    ```

## Uninstalling

=== "pipx"
    ```bash
    pipx uninstall sealkey
    ```

=== "pip"
    ```bash
    pip uninstall sealkey
    ```

## Requirements

!!! abstract "System Requirements"
    - **Python**: 3.8 or higher
    - **Operating System**: Windows, macOS, Linux
    - **Dependencies**: Automatically installed
