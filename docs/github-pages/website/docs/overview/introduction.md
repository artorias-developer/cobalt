# Introduction

Cobalt is a web dashboard for running game servers on your own VPS / VDS. It cuts out the middleman - no overpriced hosting plans, no vendor lock-in, no handing your data over to third parties. One machine, multiple games, your rules.

## Supported games 

Cobalt supports the creation of servers for a wide variety of games and their loaders. Each server runs in its own isolated Docker container. This ensures the independence of the servers and their files.

The following games are currently supported:

<div class="table games">

| Icon                                                                                                                                               | Game                  | Loaders              |
|----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|----------------------|
| <img src="https://raw.githubusercontent.com/artorias-developer/cobalt/main/cobalt/frontend/src/assets/images/games/minecraft/icon.png">            | Minecraft             | Paper, Forge, Fabric |
| <img src="https://raw.githubusercontent.com/artorias-developer/cobalt/main/cobalt/frontend/src/assets/images/games/terraria/icon.png">             | Terraria              | Vanilla, tModLoader  |
| <img src="https://raw.githubusercontent.com/artorias-developer/cobalt/main/cobalt/frontend/src/assets/images/games/dont-starve-together/icon.png"> | Don't Starve Together | Vanilla              |
| <img src="https://raw.githubusercontent.com/artorias-developer/cobalt/main/cobalt/frontend/src/assets/images/games/factorio/icon.png">             | Factorio              | Vanilla              |
| <img src="https://raw.githubusercontent.com/artorias-developer/cobalt/main/cobalt/frontend/src/assets/images/games/rim-world/icon.png">            | RimWorld              | Together             |
| <img src="https://raw.githubusercontent.com/artorias-developer/cobalt/main/cobalt/frontend/src/assets/images/games/seven-days-to-die/icon.png">    | 7 Days to Die         | Vanilla              |
| <img src="https://raw.githubusercontent.com/artorias-developer/cobalt/main/cobalt/frontend/src/assets/images/games/project-zomboid/icon.png">      | Project Zomboid       | Vanilla              |
| <img src="https://raw.githubusercontent.com/artorias-developer/cobalt/main/cobalt/frontend/src/assets/images/games/barotrauma/icon.png">           | Barotrauma            | Vanilla              |

</div>
## Features

Cobalt ships with everything you need to run and manage game servers without leaving the browser:
- Easy server management and sending game commands.
- Real-time / last 15 minutes monitoring of CPU and RAM usage for your VPS / VDS and each game server.
- Creating multiple users and roles with the ability to control access to virtually every section of the dashboard.
- A convenient file manager and editor for managing files and editing configuration files.
- Automatic fetching of the latest available game versions.
- Translation into several languages (English, Russian, Ukrainian).
- Several color themes (Dark, Light).
- Full mobile devices support.

## Core project team

<div class="table team">

| Name     | Role    | Links                                           |
|----------|---------|-------------------------------------------------|
| Artorias | Founder | [GitHub](https://github.com/artorias-developer) |

</div>


<style>
.table.games table {
  table-layout: fixed;
  width: 100%;
}

.table.games table th:nth-child(1) {
   text-align: center;
}

.table.games table th:nth-child(2) { 
   min-width: 200px; 
}

.table.games table th:nth-child(3) { 
   min-width: 200px; 
}

.table.games table td:nth-child(1) img {
   width: 36px;
   height: 36px;
   object-fit: contain;
}
</style>