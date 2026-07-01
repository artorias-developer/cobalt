# Installation

This guide explains how to install and run Cobalt on your own VPS / VDS.

## Requirements

**Operating system**: Ubuntu 22.04 LTS or newer. Other distributions are not officially supported and may require manual adjustments to the installer.

**Public IP address**: A static public IPv4 address is required so the dashboard and game servers are reachable from the internet. A dynamic IP may work but is not recommended for production use.

**Git**: Required to clone the Cobalt repository. Install it via `apt install git` if not already available on your system.

## Quick start

1. Open CMD / Terminal.

2. Connect to the server via SSH:

```bash
ssh root@<server_ip>
```

::: tip
If this is your first attempt, you will be prompted to enter "yes".
:::

3. Enter the server password.

::: tip
The letters won't appear as you type, but that's normal.
:::

4. Clone the repository:

```bash
git clone https://github.com/ArtoriasCode/cobalt
```

5. Navigate to the project directory:

```bash
cd cobalt
```

6. Make the installer executable:

```bash
chmod +x build/scripts/install.sh
```

7. Run the installer:

```bash
./build/scripts/install.sh --prod --server <server_ip>
```

:::tip
If you need to bind Cobalt to a port other than the default `443`, you can add the `--port <custom_port>` option.
:::

The installer will automatically install Docker and Docker Compose if not present, generate SSL certificates and all config files, build and start the containers.

## Dashboard access

Your dashboard will be accessible at `https://<server_ip>`.

:::tip Credentials
**Login**: `admin`

**Password**: `admin`
:::

::: warning
Since the certificates are self-signed, you'll see a security warning the first time you open the dashboard. Click `Advanced` and then `Proceed to <server_ip> (unsafe)`.
:::

::: warning
Change the default password immediately after your first login to keep your dashboard secure.
:::