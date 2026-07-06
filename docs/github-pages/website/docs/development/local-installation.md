# Local installation

This guide explains how to install Cobalt locally.

## Requirements

**Operating system**: Linux or macOS is recommended. Windows users should use WSL2, since the project relies on Unix shell scripts and Make.

**Git**: Required to clone the Cobalt repository. Install it via `apt install git` on Linux or `brew install git` on macOS.

**Make**: Used to run common development commands. Install it via your package manager, e.g. `apt install make` on Ubuntu or `brew install make` on macOS.

**Docker and Docker Compose**: Required to build and run the project's containers locally. Follow the [official installation guide](https://docs.docker.com/engine/install/) for your platform.

## First-time setup

If you haven't installed Cobalt yet, use the installer with the `--local` flag:

::: warning
The installer is officially tested on **Ubuntu 22.04+**. Other operating systems may work but aren't officially supported and could require manual adjustments.
:::

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
./build/scripts/install.sh --dev --local
```

::: tip
You can optionally pass a custom local domain, e.g. `./build/scripts/install.sh --dev --local cobalt.local`.
:::

If a domain is provided, the dashboard will be available at `https://<domain>`. Otherwise, it will be available at `https://127.0.0.1`.

:::tip Credentials
**Login**: `admin`

**Password**: `admin`
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