# Workshop

This guide explains how to download mods from the Steam Workshop and find their files on your computer.

## Game IDs

Mods downloaded by Steam are stored in folders named after numeric IDs, not game names. Use this table to find the right one.

<div class="table games">

| Icon                                                                                                                                               | Game                  | Loader     | Steam ID  |
|----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|------------|-----------|
| <img src="https://raw.githubusercontent.com/artorias-developer/cobalt/main/cobalt/frontend/src/assets/images/games/terraria/icon.png">             | Terraria              | tModLoader | `1281930` |
| <img src="https://raw.githubusercontent.com/artorias-developer/cobalt/main/cobalt/frontend/src/assets/images/games/dont-starve-together/icon.png"> | Don't Starve Together | Vanilla    | `322330`  |
| <img src="https://raw.githubusercontent.com/artorias-developer/cobalt/main/cobalt/frontend/src/assets/images/games/rim-world/icon.png">            | RimWorld              | Together   | `294100`  |
| <img src="https://raw.githubusercontent.com/artorias-developer/cobalt/main/cobalt/frontend/src/assets/images/games/project-zomboid/icon.png">      | Project Zomboid       | Vanilla    | `108600`  |
| <img src="https://raw.githubusercontent.com/artorias-developer/cobalt/main/cobalt/frontend/src/assets/images/games/barotrauma/icon.png">           | Barotrauma            | Vanilla    | `602960`  |

</div>

Games without Steam Workshop support are not covered by this guide. Install their mods using the method described in the game's own documentation.

## Downloading mods

1. Open the mod's page in the Steam Workshop.

2. Click the subscribe button.

3. Make sure Steam has finished downloading the mod. You can check the progress in the downloads tab of the Steam client.

4. Note the mod ID from the URL:

```
https://steamcommunity.com/sharedfiles/filedetails/?id=1234567890
```

Here, `1234567890` is the mod ID. Authors also sometimes include the mod ID and Steam Workshop ID at the very end of the description.

## Finding mod files

There are two ways to find the downloaded mod files.

::: warning
The contents of a mod folder differ between games. In some games a mod is a whole folder, in others it is a single file that must be taken out of the folder and used on its own. Check the guide for your specific game to see what exactly you need to upload and how.
:::

### Manually

Mods are stored locally in the following directory:

```
<steam_folder>/steamapps/workshop/content/<game_id>/<mod_id>
```

Below are the default Steam folder locations. If you installed Steam or the game to a custom location, the `steamapps` folder will be located in that library folder instead.

<div class="table paths">

| OS      | Path                                  |
|---------|---------------------------------------|
| Windows | `C:\Program Files (x86)\Steam`        |
| Linux   | `~/.steam/steam`                      |
| macOS   | `~/Library/Application Support/Steam` |

</div>

For example, a Terraria mod with the ID `1234567890` on Windows will be located at:

```
C:\Program Files (x86)\Steam\steamapps\workshop\content\1281930\1234567890
```

The game ID `1281930` is taken from the [Game IDs](#game-ids) table above, and the mod ID `1234567890` is the one you noted in the mod's page URL.

### Via Steam

1. Right-click the game in your Steam library.

2. Click the manage button.

3. Click the browse local files button.

4. Go up to the `steamapps` folder in the file manager.

5. Open the `workshop/content` folder in the file manager.

<style>
.table.games table {
  table-layout: fixed;
  width: 100%;
}

.table.games table th:nth-child(1) {
  width: 36px;
  text-align: center;
}

.table.games table th:nth-child(2) {
  min-width: 200px;
}

.table.games table th:nth-child(3) {
  min-width: 120px;
}

.table.games table th:nth-child(4) {
  min-width: 100px;
}

.table.games table td:nth-child(1) img {
  width: 36px;
  height: 36px;
  object-fit: contain;
}

.table.paths table {
  table-layout: fixed;
  width: 100%;
}

.table.paths table td:nth-child(2) {
  word-break: break-all;
}

.table.paths table th:nth-child(1) {
  min-width: 100px;
}

.table.paths table th:nth-child(2) {
  min-width: 200px;
}
</style>