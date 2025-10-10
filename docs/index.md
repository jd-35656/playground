# SealKey: Seal Your Secrets. Unlock with Confidence

SealKey is a lightweight and secure Python tool designed to manage your sensitive data. It uses AES-256 encryption to keep your secrets safe and stores the master key securely in your OS's keychain (macOS Keychain, Windows Credential Manager, Linux SecretService). Encrypted secrets are stored in a secure JSON file, ensuring both ease of access and maximum security.

## Features

* **AES-256 encryption**: Strong encryption to protect your data.
* **Secure master key storage**: Stored in your OS’s keyring (macOS Keychain, Windows Credential Manager, Linux SecretService).
* **Encrypted data storage**: Secrets are stored securely in a JSON file.
* **Core CLI commands**: Lock, unlock, add, remove, update, and list secrets.
* **Cross-platform**: Compatible with macOS, Windows, and Linux.

## Installation

To install SealKey, run:

```bash
pip install sealkey
```

## Usage

### Command-Line Interface (CLI)

SealKey provides simple commands to manage your encrypted secrets. For detailed usage and examples, visit the full documentation:

[**SealKey Documentation**](https://jd-35656.github.io/sealkey)

#### CLI Commands

* **Unlock Secret Vault**: Adds the decryption key for the Vault to the OS keychain after performing an integrity check and initializes the Vault if it doesn't already exist.

  ```bash
  sealkey unlock
  ```

> **Note**: This command will prompt you to enter your master password for security.

* **Add a secret**: Add a new secret to the secure JSON vault (if it doesn’t already exist).

  ```bash
  sealkey add <SecretGroup> <SecretLabel>
  ```

> **Note**: You will be prompted to enter the secret value.

* **Remove a secret**: Remove a secret or an entire secret group from the secure JSON vault.

  ```bash
  sealkey remove <SecretGroup> <SecretLabel>
  sealkey remove <SecretGroup>
  ```

> **Note**: You will be asked for confirmation before removal.

* **Update a secret**: Update the value of an existing secret.

  ```bash
  sealkey update <SecretGroup> <SecretLabel>
  ```

> **Note**: You will be prompted to enter the new secret value.

* **List secrets**: List all stored secrets or secrets within a specific category.

  ```bash
  sealkey list
  sealkey list <SecretGroup>
  ```

* **Lock Secret Vault**: Removes the decryption key from the OS keychain, effectively locking the Vault.

  ```bash
  sealkey lock
  ```

---

### Python Library Usage

You can integrate SealKey directly into your Python projects for programmatic access to your secrets.

Here’s how you can use the SealKey Python library:

#### Unlock the Vault

To unlock the secret vault and add the decryption key to the OS keychain, call the `unlock()` function.

```python
import sealkey

# Unlock the secret vault using a master key
sealkey.unlock(master_key='your_secure_master_key')
```

* **Parameters**:

  * `master_key`: The master key used to decrypt and access the secret vault.

#### Lock the Vault

To lock the vault and remove the decryption key from the OS keychain, call the `lock()` function.

```python
# Lock the secret vault
sealkey.lock()
```

#### Add a Secret

Add a new secret to the secure JSON vault using the `add()` function.

```python
# Add a new secret to the vault
sealkey.add(secret_group="MySecretGroup", secret_label="mySecretLabel", secret_value="MySecretValue")
```

* **Parameters**:

  * `secret_group`: The group or category where the secret should be stored.
  * `secret_label`: A unique label/identifier for the secret.
  * `secret_value`: The actual secret value to store.

#### Remove a Secret

To remove a specific secret or an entire secret group, use the `remove()` function.

```python
# Remove a specific secret from the vault
sealkey.remove(secret_group="MySecretGroup", secret_label="mySecretLabel")

# Remove all secrets in a group
sealkey.remove(secret_group="MySecretGroup")
```

* **Parameters**:

  * `secret_group`: The group where the secret is stored.
  * `secret_label`: The label of the specific secret to remove (optional).

#### Update a Secret

To update an existing secret, use the `update()` function.

```python
# Update an existing secret in the vault
sealkey.update(secret_group="MySecretGroup", secret_label="mySecretLabel", secret_value="UpdatedSecretValue")
```

* **Parameters**:

  * `secret_group`: The group of the secret to update.
  * `secret_label`: The label of the secret to update.
  * `secret_value`: The new value for the secret.

#### List Secrets

To list all stored secrets or secrets from a specific group, use the `list()` function.

```python
# List all secrets
secrets = sealkey.list()
print(secrets)

# List secrets from a specific group
secrets_in_group = sealkey.list(secret_group="MySecretGroup")
print(secrets_in_group)
```

* **Parameters**:

  * `secret_group`: (Optional) If specified, only secrets within this group are listed.

---

### Secure Data Storage

* The **master key** is securely stored in the OS keychain.
* All **secrets** are encrypted and stored in a secure JSON file.

## License

`sealkey` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Contact

Created by Jitesh Sahani (JD)
Email: [jitesh.sahani@outlook.com](mailto:jitesh.sahani@outlook.com)
