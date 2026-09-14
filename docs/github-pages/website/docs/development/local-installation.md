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

:::details List of available flags

<div class="table flags">

| Flag                 | Required                | Description                                                                                                                                                               |
|----------------------|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --prod               | no                      | Use production environment. Defaults to `--prod` if neither `--prod` nor `--dev` is provided.                                                                             |
| --dev                | no                      | Use development environment.                                                                                                                                              |
| --local [domain]     | yes (or use `--server`) | Deploy locally. Defaults to `127.0.0.1` if domain is not provided.                                                                                                        |
| --server &lt;ip&gt;  | yes (or use `--local`)  | An IP or a domain name of the VPS / VDS.                                                                                                                                  |
| --port &lt;port&gt;  | no                      | HTTPS port to use. Defaults to `443` if not provided.                                                                                                                     |                                                                                                               |
| --no-admin-base      | no                      | By default the dashboard page is hidden behind a random, hard-to-guess URL for extra security. Use this flag to disable that and use a normal, predictable URL instead.   |
</div>
:::

The installer will automatically install Docker and Docker Compose if not present, generate SSL certificates and all config files, build and start the containers.

:::tip
A link to the dashboard and login credentials will be displayed after installation.
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