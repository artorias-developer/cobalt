# Installation

## Requirements

- VPS / VDS running **Ubuntu 22+**
- A public IP address

## Installation

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

The installer will automatically install Docker and Docker Compose if not present, generate SSL certificates and all config files, build and start the containers.

::: tip
Your dashboard will be accessible at `https://<server_ip>`, using the default login and password `admin`.
:::

::: warning
Since the certificates are self-signed, you'll see a security warning the first time you open the dashboard. Click `Advanced` and then `Proceed to <server_ip> (unsafe)`.
:::