# Introduction

Cobalt is a web dashboard for running game servers on your own VPS / VDS. It cuts out the middleman - no overpriced hosting plans, no vendor lock-in, no handing your data over to third parties. One machine, multiple games, your rules.

## Supported games 

Cobalt supports the creation of servers for a wide variety of games and their loaders. Each server runs in its own isolated Docker container. This ensures the independence of the servers and their files.

The following games are currently supported:

<table>
  <thead>
    <tr>
      <th style="text-align: center">Icon</th>
      <th>Game</th>
      <th>Loaders</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="display: flex;justify-content: center;"><img src="https://raw.githubusercontent.com/ArtoriasCode/cobalt/main/cobalt/frontend/src/assets/images/games/minecraft/icon.png" style="height: 30px"></td>
      <td>Minecraft</td>
      <td>Paper, Forge, Fabric</td>
    </tr>
    <tr>
      <td style="display: flex;justify-content: center;"><img src="https://raw.githubusercontent.com/ArtoriasCode/cobalt/main/cobalt/frontend/src/assets/images/games/terraria/icon.png" style="height: 30px"></td>
      <td>Terraria</td>
      <td>Vanilla, tModLoader</td>
    </tr>
    <tr>
      <td style="display: flex;justify-content: center;"><img src="https://raw.githubusercontent.com/ArtoriasCode/cobalt/main/cobalt/frontend/src/assets/images/games/dont-starve-together/icon.png" style="height: 30px"></td>
      <td>Don't Starve Together</td>
      <td>Vanilla</td>
    </tr>
    <tr>
      <td style="display: flex;justify-content: center;"><img src="https://raw.githubusercontent.com/ArtoriasCode/cobalt/main/cobalt/frontend/src/assets/images/games/factorio/icon.png" style="height: 30px"></td>
      <td>Factorio</td>
      <td>Vanilla</td>
    </tr>
    <tr>
      <td style="display: flex;justify-content: center;"><img src="https://raw.githubusercontent.com/ArtoriasCode/cobalt/main/cobalt/frontend/src/assets/images/games/rim-world/icon.png" style="height: 30px"></td>
      <td>RimWorld</td>
      <td>Together</td>
    </tr>
    <tr>
      <td style="display: flex;justify-content: center;"><img src="https://raw.githubusercontent.com/ArtoriasCode/cobalt/main/cobalt/frontend/src/assets/images/games/seven-days-to-die/icon.png" style="height: 30px"></td>
      <td>7 Days to Die</td>
      <td>Vanilla</td>
    </tr>
    <tr>
      <td style="display: flex;justify-content: center;"><img src="https://raw.githubusercontent.com/ArtoriasCode/cobalt/main/cobalt/frontend/src/assets/images/games/project-zomboid/icon.png" style="height: 30px"></td>
      <td>Project Zomboid</td>
      <td>Vanilla</td>
    </tr>
  </tbody>
</table>

## Features

Cobalt ships with everything you need to run and manage game servers without leaving the browser:
- Easy server management and sending game commands.
- Real-time / last 15 minutes monitoring of CPU and RAM usage for your VPS / VDS and each game server.
- Creating multiple users and roles with the ability to control access to virtually every section of the dashboard.
- A convenient file manager and editor for managing files and editing configuration files.
- Automatic fetching of the latest available game versions.
- Multilingual support (English, Russian, Ukrainian).
- Full mobile devices support.

## Core project team

| Name         | Role                         | Links                                     |
|--------------|------------------------------|-------------------------------------------|
| ArtoriasCode | Founder & Project Maintainer | [GitHub](https://github.com/ArtoriasCode) |