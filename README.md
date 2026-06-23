<div align="center">
  <img src="docs/readme/images/logo.svg" alt="Cobalt" width="400">

  <h3>Self-hosted game servers dashboard for friend groups</h3>

  [![License](https://img.shields.io/badge/License-AGPL--3.0-blue)](https://github.com/ArtoriasCode/cobalt/blob/main/LICENSE)
  [![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
  [![Vue](https://img.shields.io/badge/Vue-4FC08D?logo=vuedotjs&logoColor=white)](https://vuejs.org/)
  [![Wiki](https://img.shields.io/badge/Wiki-grey?logo=gitbook&logoColor=white)](https://artoriascode.github.io/cobalt/)
</div>

---

## What is Cobalt?

Cobalt is a web dashboard for running game servers on your own VPS / VDS. It cuts out the middleman - no overpriced hosting plans, no vendor lock-in, no handing your data over to third parties. One machine, multiple games, your rules.

<details>
<summary><ins>Dashboard screenshots</ins></summary>

<img src="docs/readme/images/cobalt/1.png" width="100%">
<img src="docs/readme/images/cobalt/2.png" width="100%">
<img src="docs/readme/images/cobalt/3.png" width="100%">
<img src="docs/readme/images/cobalt/4.png" width="100%">
<img src="docs/readme/images/cobalt/5.png" width="100%">
<img src="docs/readme/images/cobalt/6.png" width="100%">
<img src="docs/readme/images/cobalt/7.png" width="100%">

</details>

## Getting started

Whether you're setting up Cobalt for the first time or looking to contribute, the links below cover everything you need - from installation guides to community discussions where you can share ideas and vote on new game support.

- [Documentation](https://artoriascode.github.io/cobalt/) - installation, testing and more.
- [Issues](https://github.com/ArtoriasCode/cobalt/issues) - report bugs and problems.
- [Ideas](https://github.com/ArtoriasCode/cobalt/discussions/categories/ideas) - share your ideas and suggest new games.
- [Help](https://github.com/ArtoriasCode/cobalt/discussions/categories/help) - ask your questions.

> [!WARNING]
> Before posting anything, please read the guidelines.

## Supported games

Cobalt supports the creation of servers for a wide variety of games and their loaders. Each server runs in its own isolated Docker container. This ensures the independence of the servers and their files.

The following games are currently supported:

|                                              Icon                                              | Game                  | Loaders              |
|:----------------------------------------------------------------------------------------------:|-----------------------|----------------------|
|       <img src="cobalt/frontend/src/assets/images/games/minecraft/icon.png" height="30">       | Minecraft             | Paper, Forge, Fabric |
|       <img src="cobalt/frontend/src/assets/images/games/terraria/icon.png" height="30">        | Terraria              | Vanilla, tModLoader  |
| <img src="cobalt/frontend/src/assets/images/games/dont-starve-together/icon.png" height="30">  | Don't Starve Together | Vanilla              |
|       <img src="cobalt/frontend/src/assets/images/games/factorio/icon.png" height="30">        | Factorio              | Vanilla              |
|       <img src="cobalt/frontend/src/assets/images/games/rim-world/icon.png" height="30">       | RimWorld              | Together             |
|   <img src="cobalt/frontend/src/assets/images/games/seven-days-to-die/icon.png" height="30">   | 7 Days to Die         | Vanilla              |

## Features

Cobalt ships with everything you need to run and manage game servers without leaving the browser:
- Easy server management and sending game commands.
- Real-time / last 15 minutes monitoring of CPU and RAM usage for your VPS / VDS and each game server.
- Creating multiple users and roles with the ability to control access to virtually every section of the dashboard.
- A convenient file manager and editor for managing files and editing configuration files.
- Automatic fetching of the latest available game versions.
- Multilingual support (English, Russian, Ukrainian).
- Full mobile devices support.

## FAQ

<details>
<summary>Where can I get a VPS / VDS?</summary>

Any VPS / VDS provider works. Just make sure it runs Ubuntu 22+.

</details>

<details>
<summary>What does the dashboard look like?</summary>

<img src="docs/readme/images/cobalt/1.png" width="100%">
<img src="docs/readme/images/cobalt/2.png" width="100%">
<img src="docs/readme/images/cobalt/3.png" width="100%">
<img src="docs/readme/images/cobalt/4.png" width="100%">
<img src="docs/readme/images/cobalt/5.png" width="100%">
<img src="docs/readme/images/cobalt/6.png" width="100%">
<img src="docs/readme/images/cobalt/7.png" width="100%">

</details>

<details>
<summary>How can I support the project financially?</summary>

|                                  Icon                                   | Token | Network | Address |
|:-----------------------------------------------------------------------:|-------|---------|---------|
| <img src="cobalt/frontend/src/assets/images/svg/usdc.svg" height="20">  | USDC | ERC20 / BEP20 | `0x0C24ee1cDC35824390879Bd8A7235c473FCEcEDC` |
| <img src="cobalt/frontend/src/assets/images/svg/usdc.svg" height="20">  | USDC | SPL | `7gUG9Xz94V7nBEdC37DD5fhH75L6qQxRmnpke19tQVZP` |
| <img src="cobalt/frontend/src/assets/images/svg/usdt.svg" height="20">  | USDT | ERC20 / BEP20 | `0x0C24ee1cDC35824390879Bd8A7235c473FCEcEDC` |
| <img src="cobalt/frontend/src/assets/images/svg/usdt.svg" height="20">  | USDT | SPL | `7gUG9Xz94V7nBEdC37DD5fhH75L6qQxRmnpke19tQVZP` |
| <img src="cobalt/frontend/src/assets/images/svg/usdt.svg" height="20">  | USDT | TRC20 | `TK85QzUhftZmm3rfDreWnVi5Q5eE5t42e1` |
|  <img src="cobalt/frontend/src/assets/images/svg/btc.svg" height="20">  | BTC | Bitcoin | `bc1qnw605zwkz6jz23fsydxmzms7tsh7jwp2kaumjw` |
|  <img src="cobalt/frontend/src/assets/images/svg/eth.svg" height="20">  | ETH | Ethereum | `0x0C24ee1cDC35824390879Bd8A7235c473FCEcEDC` |
|  <img src="cobalt/frontend/src/assets/images/svg/bnb.svg" height="20">  | BNB | BNB Smart Chain | `0x0C24ee1cDC35824390879Bd8A7235c473FCEcEDC` |
|  <img src="cobalt/frontend/src/assets/images/svg/sol.svg" height="20">  | SOL | Solana | `7gUG9Xz94V7nBEdC37DD5fhH75L6qQxRmnpke19tQVZP` |

</details>