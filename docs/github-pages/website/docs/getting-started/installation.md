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
git clone https://github.com/artorias-developer/cobalt
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

:::details List of available flags

<div class="table flags">

| Flag                 | Required                | Description                                                                                                                                                        |
|----------------------|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --prod               | no                      | Use production environment. Defaults to `--prod` if neither `--prod` nor `--dev` is provided.                                                                      |
| --dev                | no                      | Use development environment.                                                                                                                                       |
| --local [domain]     | yes (or use `--server`) | Deploy locally. Defaults to `127.0.0.1` if domain is not provided.                                                                                                 |
| --server &lt;ip&gt;  | yes (or use `--local`)  | An IP or a domain name of the VPS / VDS.                                                                                                                           |
| --port &lt;port&gt;  | no                      | HTTPS port to use. Defaults to `443` if not provided.                                                                                                              |                                                                                                               |
| --no-admin-base      | no                      | By default the dashboard is hidden behind a random, hard-to-guess URL for extra security. Use this flag to disable that and use a normal, predictable URL instead. |
</div>
:::

## Dashboard access

A link to the dashboard and login credentials will be displayed after installation.

::: warning
Since the certificates are self-signed, you'll see a security warning the first time you open the dashboard. Click `Advanced` and then `Proceed to <server_ip> (unsafe)`.
:::

::: warning
Change the default password immediately after your first login to keep your dashboard secure.
:::

<style>
table {
  table-layout: fixed;
  width: 100%;
}

table td:nth-child(1),
table td:nth-child(3) {
   word-break: break-all;
}

table th:nth-child(1) { 
   min-width: 150px; 
}

table th:nth-child(2) { 
   min-width: 90px; 
}

table th:nth-child(3) { 
   min-width: 150px; 
}
</style>