# Local installation

This guide explains how to install Cobalt locally.

## Requirements

#### Operating system

The following operating systems are supported. Other distributions are not officially supported and may not work or may require manual adjustments to the installer.

| OS     | Supported versions      |
|--------|-------------------------|
| Ubuntu | 22.04 LTS or newer      |
| Debian | 13 (Trixie) or newer    |

---

#### git

Required for cloning the Cobalt repository.

::: code-group
```bash [Ubuntu]
apt install git
```

```bash [Debian]
apt install git
```
:::

---

#### make

Used to run common development commands.

::: code-group
```bash [Ubuntu]
apt install make
```

```bash [Debian]
apt install make
```
:::

## First-time setup

1. Clone the repository:

```bash
git clone https://github.com/artorias-developer/cobalt
```

2. Navigate to the project directory:

```bash
cd cobalt
```

3. Make the installer executable:

```bash
chmod +x build/scripts/install.sh
```

4. Run the installer in local mode:

```bash
./build/scripts/install.sh
```

The installer will ask you for some details, and then it will take care of everything automatically.

## Dashboard access

A link to the dashboard and login credentials will be displayed after installation.

::: warning
Since the certificates are self-signed, you'll see a security warning the first time you open the dashboard. Click `Advanced` and then `Proceed to <server_ip> (unsafe)`.
:::

## Makefile commands

If you've already installed Cobalt before, you can manage the development environment directly using the [Makefile](https://github.com/artorias-developer/cobalt/blob/main/Makefile) commands:

```bash
# Start the dev containers
make docker-build-dev

# Rebuild and start the dev containers
make docker-rebuild-dev

# Stop the dev containers
make docker-down-dev
```

::: tip
Short aliases are also available, e.g. `make d:b:d`, `make d:r:d`, `make d:d:d`.
:::