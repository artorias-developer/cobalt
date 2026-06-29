# 7 Days to Die

This tutorial explains how to set up 7 Days to Die server in the Cobalt dashboard.

## Changing configs

1. Open the servers page.

2. Find the server you want to change settings in the table and click the first button in the actions column.

3. Open the files tab at the top.

   ---

   ### `serverconfig.xml`

   1. Open the `serverconfig.xml` file in the file editor.

   2. Update the settings.

   :::details List of settings
   
   This table refers to version `23906567`. Some settings may not be available in earlier versions. Cobalt overrides some default values when a server is created.
   
   | Key                                  | Type    | Default            | Description                                                                                                                                                                    |
   |--------------------------------------|---------|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
   | `ServerName`                         | string  | `My 7DTD Server`   | Name of the server as it appears in the server browser.                                                                                                                        |
   | `ServerDescription`                  | string  | _(blank)_          | Server description shown in the server browser.                                                                                                                                |
   | `ServerWebsiteURL`                   | string  | _(blank)_          | Website URL shown in the server browser as a clickable link.                                                                                                                   |
   | `ServerPassword`                     | string  | _(blank)_          | Password required to join the server.                                                                                                                                          |
   | `ServerLoginConfirmationText`        | string  | _(blank)_          | Message shown to the user during join that must be confirmed before continuing.                                                                                                |
   | `Region`                             | string  | `NorthAmericaEast` | The region this server is in. Values: `NorthAmericaEast`, `NorthAmericaWest`, `CentralAmerica`, `SouthAmerica`, `Europe`, `Russia`, `Asia`, `MiddleEast`, `Africa`, `Oceania`. |
   | `Language`                           | string  | `English`          | Primary language for players on this server.                                                                                                                                   |
   | `ServerPort`                         | integer | `26900`            | Port the server listens on. Keep in ranges 26900-26905 or 27015-27020 for LAN discovery.                                                                                       |
   | `ServerVisibility`                   | integer | `2`                | Visibility of the server:<br>`2` - public<br>`1` - friends only<br>`0` - not listed                                                                                            |
   | `ServerDisabledNetworkProtocols`     | string  | `SteamNetworking`  | Networking protocols to disable, separated by comma. Possible values: `LiteNetLib`, `SteamNetworking`.                                                                         |
   | `ServerMaxWorldTransferSpeedKiBs`    | integer | `512`              | Maximum speed in KiB/s at which the world is transferred to a client on first connect. Max ~1300 KiB/s.                                                                        |
   | `ServerMaxPlayerCount`               | integer | `8`                | Maximum number of concurrent players.                                                                                                                                          |
   | `ServerReservedSlots`                | integer | `0`                | Number of slots reserved for players with a specific permission level.                                                                                                         |
   | `ServerReservedSlotsPermission`      | integer | `100`              | Permission level required to use reserved slots.                                                                                                                               |
   | `ServerAdminSlots`                   | integer | `0`                | Number of admin slots that allow joining even when the server is full.                                                                                                         |
   | `ServerAdminSlotsPermission`         | integer | `0`                | Permission level required to use admin slots.                                                                                                                                  |
   | `WebDashboardEnabled`                | boolean | `false`            | Enables or disables the web dashboard.                                                                                                                                         |
   | `WebDashboardPort`                   | integer | `8080`             | Port of the web dashboard.                                                                                                                                                     |
   | `WebDashboardUrl`                    | string  | _(blank)_          | External URL to the web dashboard if behind a reverse proxy. Must be the full URL.                                                                                             |
   | `EnableMapRendering`                 | boolean | `false`            | Enables rendering of the map to tile images while exploring. Used by the web dashboard.                                                                                        |
   | `TelnetEnabled`                      | boolean | `true`             | Enables or disables the Telnet interface.                                                                                                                                      |
   | `TelnetPort`                         | integer | `8081`             | Port of the Telnet server.                                                                                                                                                     |
   | `TelnetPassword`                     | string  | _(blank)_          | Password for the Telnet interface. If blank, listens on local loopback only.                                                                                                   |
   | `TelnetFailedLoginLimit`             | integer | `10`               | Number of wrong passwords from a single client before it is blocked from Telnet.                                                                                               |
   | `TelnetFailedLoginsBlocktime`        | integer | `10`               | How long the block persists in seconds.                                                                                                                                        |
   | `TerminalWindowEnabled`              | boolean | `true`             | Shows a terminal window for log output and command input. Windows only.                                                                                                        |
   | `AdminFileName`                      | string  | `serveradmin.xml`  | Server admin file name. Path relative to `UserDataFolder/Saves`.                                                                                                               |
   | `ServerAllowCrossplay`               | boolean | `false`            | Enables or disables crossplay.                                                                                                                                                 |
   | `EACEnabled`                         | boolean | `true`             | Enables or disables EasyAntiCheat.                                                                                                                                             |
   | `IgnoreEOSSanctions`                 | boolean | `false`            | If enabled, ignores EOS sanctions when allowing players to join.                                                                                                               |
   | `HideCommandExecutionLog`            | integer | `0`                | Hide logging of command execution.<br>`0` - show everything<br>`1` - hide from Telnet/ControlPanel<br>`2` - also hide from remote clients<br>`3` - hide everything             |
   | `MaxUncoveredMapChunksPerPlayer`     | integer | `131072`           | Overrides how many chunks can be uncovered on the map per player.                                                                                                              |
   | `PersistentPlayerProfiles`           | boolean | `false`            | If enabled, players join with the last profile they used.                                                                                                                      |
   | `MaxChunkAge`                        | integer | `-1`               | In-game days before an unvisited chunk resets. `-1` disables.                                                                                                                  |
   | `SaveDataLimit`                      | integer | `-1`               | Maximum disk space per saved game in MB. Negative values disable the limit.                                                                                                    |
   | `GameWorld`                          | string  | `Navezgane`        | World to load. Use `RWG` for random gen or an existing world name.                                                                                                             |
   | `WorldGenSeed`                       | string  | `Cobalt`           | Seed for RWG world generation.                                                                                                                                                 |
   | `WorldGenSize`                       | integer | `6144`             | Width and height of the RWG world. Supported values: `6144`, `8192`, `10240`.                                                                                                  |
   | `GameName`                           | string  | `Cobalt`           | Name of the game/save. Affects save name and decoration seed.                                                                                                                  |
   | `GameMode`                           | string  | `GameModeSurvival` | Game mode.                                                                                                                                                                     |
   | `GameDifficulty`                     | integer | `1`                | Difficulty level.<br>`0` - easiest<br>`5` - hardest                                                                                                                            |
   | `BlockDamagePlayer`                  | integer | `100`              | How much damage players deal to blocks, in percent.                                                                                                                            |
   | `BlockDamageAI`                      | integer | `100`              | How much damage AIs deal to blocks, in percent.                                                                                                                                |
   | `BlockDamageAIBM`                    | integer | `100`              | How much damage AIs deal to blocks during blood moons, in percent.                                                                                                             |
   | `XPMultiplier`                       | integer | `100`              | XP gain multiplier in percent.                                                                                                                                                 |
   | `PlayerSafeZoneLevel`                | integer | `5`                | Players at or below this level get a safe zone (no enemies) on spawn.                                                                                                          |
   | `PlayerSafeZoneHours`                | integer | `5`                | Duration of the safe zone in in-game hours.                                                                                                                                    |
   | `BuildCreate`                        | boolean | `false`            | Enables or disables cheat mode.                                                                                                                                                |
   | `DayNightLength`                     | integer | `60`               | Real-time minutes per in-game day.                                                                                                                                             |
   | `DayLightLength`                     | integer | `18`               | In-game hours of sunlight per day.                                                                                                                                             |
   | `BiomeProgression`                   | boolean | `true`             | Enables biome hazards. Weather and storms are not affected.                                                                                                                    |
   | `StormFreq`                          | integer | `100`              | Frequency of storms in percent. `0` turns them off.                                                                                                                            |
   | `DeathPenalty`                       | integer | `1`                | Penalty on death.<br>`0` - nothing<br>`1` - XP penalty<br>`2` - injured<br>`3` - permanent death                                                                               |
   | `DropOnDeath`                        | integer | `1`                | What is dropped on death.<br>`0` - nothing<br>`1` - everything<br>`2` - toolbelt only<br>`3` - backpack only<br>`4` - delete all                                               |
   | `DropOnQuit`                         | integer | `0`                | What is dropped on quit.<br>`0` - nothing<br>`1` - everything<br>`2` - toolbelt only<br>`3` - backpack only                                                                    |
   | `BedrollDeadZoneSize`                | integer | `15`               | Box radius of the bedroll dead zone where no zombies spawn.                                                                                                                    |
   | `BedrollExpiryTime`                  | integer | `45`               | Real-world days a bedroll stays active after the owner was last online.                                                                                                        |
   | `AllowSpawnNearFriend`               | integer | `2`                | Whether new players can spawn near a friend.<br>`0` - disabled<br>`1` - always<br>`2` - forest biome only                                                                      |
   | `CameraRestrictionMode`              | integer | `0`                | Camera mode restriction.<br>`0` - free<br>`1` - first person only<br>`2` - third person only                                                                                   |
   | `JarRefund`                          | integer | `60`               | Empty jar refund percentage after consuming an item.                                                                                                                           |
   | `MaxSpawnedZombies`                  | integer | `64`               | Maximum number of zombies alive across the entire map at once.                                                                                                                 |
   | `MaxSpawnedAnimals`                  | integer | `50`               | Maximum number of animals alive across the entire map at once.                                                                                                                 |
   | `ServerMaxAllowedViewDistance`       | integer | `12`               | Maximum view distance a client may request, in chunks. Range: `6`-`12`.                                                                                                        |
   | `MaxQueuedMeshLayers`                | integer | `1000`             | Maximum chunk mesh layers enqueued during mesh generation.                                                                                                                     |
   | `EnemySpawnMode`                     | boolean | `true`             | Enables or disables enemy spawning.                                                                                                                                            |
   | `EnemyDifficulty`                    | integer | `0`                | Enemy difficulty.<br>`0` - normal<br>`1` - feral                                                                                                                               |
   | `ZombieFeralSense`                   | integer | `0`                | Feral sense mode.<br>`0` - off<br>`1` - day<br>`2` - night<br>`3` - all                                                                                                        |
   | `ZombieMove`                         | integer | `0`                | Zombie movement speed during the day.<br>`0` - walk<br>`1` - jog<br>`2` - run<br>`3` - sprint<br>`4` - nightmare                                                               |
   | `ZombieMoveNight`                    | integer | `3`                | Zombie movement speed during the night.<br>`0` - walk<br>`1` - jog<br>`2` - run<br>`3` - sprint<br>`4` - nightmare                                                             |
   | `ZombieFeralMove`                    | integer | `3`                | Feral zombie movement speed.<br>`0` - walk<br>`1` - jog<br>`2` - run<br>`3` - sprint<br>`4` - nightmare                                                                        |
   | `ZombieBMMove`                       | integer | `3`                | Blood moon zombie movement speed.<br>`0` - walk<br>`1` - jog<br>`2` - run<br>`3` - sprint<br>`4` - nightmare                                                                   |
   | `AISmellMode`                        | integer | `3`                | AI smell detection mode.<br>`0` - off<br>`1` - walk<br>`2` - jog<br>`3` - run<br>`4` - sprint<br>`5` - nightmare                                                               |
   | `BloodMoonFrequency`                 | integer | `7`                | Frequency of blood moons in days.<br>`0` - disabled                                                                                                                            |
   | `BloodMoonRange`                     | integer | `0`                | Random deviation in days from the blood moon schedule.<br>`0` - exact                                                                                                          |
   | `BloodMoonWarning`                   | integer | `8`                | In-game hour when the red day number appears on a blood moon day.<br>`-1` - never                                                                                              |
   | `BloodMoonEnemyCount`                | integer | `8`                | Number of zombies that can be alive per player during a blood moon. Overridden by `MaxSpawnedZombies` in multiplayer.                                                          |
   | `LootAbundance`                      | integer | `100`              | Loot abundance in percent.                                                                                                                                                     |
   | `LootRespawnDays`                    | integer | `7`                | Number of days before loot respawns.                                                                                                                                           |
   | `AirDropFrequency`                   | integer | `72`               | How often airdrops occur in in-game hours.<br>`0` - never                                                                                                                      |
   | `AirDropMarker`                      | boolean | `true`             | Adds a marker to the map and compass for airdrops.                                                                                                                             |
   | `PartySharedKillRange`               | integer | `100`              | Distance in blocks within which party members share kill XP and quest credit.                                                                                                  |
   | `PlayerKillingMode`                  | integer | `3`                | PvP setting.<br>`0` - no killing<br>`1` - allies only<br>`2` - strangers only<br>`3` - everyone                                                                                |
   | `LandClaimCount`                     | integer | `5`                | Maximum land claims per player.                                                                                                                                                |
   | `LandClaimSize`                      | integer | `41`               | Size in blocks protected by a keystone.                                                                                                                                        |
   | `LandClaimDeadZone`                  | integer | `30`               | Minimum distance in blocks between keystones of different players.                                                                                                             |
   | `LandClaimExpiryTime`                | integer | `7`                | Real-world days before an offline player's claims expire.                                                                                                                      |
   | `LandClaimDecayMode`                 | integer | `0`                | How offline land claims decay.<br>`0` - slow/linear<br>`1` - fast/exponential<br>`2` - none                                                                                    |
   | `LandClaimOnlineDurabilityModifier`  | integer | `4`                | Block hardness multiplier in a claim when the owner is online.<br>`0` - infinite                                                                                               |
   | `LandClaimOfflineDurabilityModifier` | integer | `4`                | Block hardness multiplier in a claim when the owner is offline.<br>`0` - infinite                                                                                              |
   | `LandClaimOfflineDelay`              | integer | `0`                | Minutes after logout before claim hardness transitions from online to offline.                                                                                                 |
   | `DynamicMeshEnabled`                 | boolean | `true`             | Enables or disables the Dynamic Mesh system.                                                                                                                                   |
   | `DynamicMeshLandClaimOnly`           | boolean | `true`             | Restricts Dynamic Mesh to player land claim areas only.                                                                                                                        |
   | `DynamicMeshLandClaimBuffer`         | integer | `3`                | Dynamic Mesh LCB chunk radius.                                                                                                                                                 |
   | `DynamicMeshMaxItemCache`            | integer | `3`                | Maximum concurrently processed Dynamic Mesh items. Higher values use more RAM.                                                                                                 |
   | `TwitchServerPermission`             | integer | `90`               | Required permission level to use Twitch integration on the server.                                                                                                             |
   | `TwitchBloodMoonAllowed`             | boolean | `false`            | Whether Twitch actions are allowed during a blood moon. May cause lag.                                                                                                         |
   | `QuestProgressionDailyLimit`         | integer | `4`                | Maximum quests contributing to tier progression per player per day.                                                                                                            |
   :::

   :::warning
   Do not change the `ServerPort` and `TelnetPort` settings.
   :::

    3. Click the save button in the bottom left corner.

   ---

4. Open the overview tab at the top.

5. Click the restart button in the control block.

## Adding mods

:::warning
Make sure you have disabled EAC (Easy Anti-Cheat) on your computer before launching the game.
:::

1. Open the servers page.

2. Find the server you want to add mods in the table and click the first button in the actions column.

3. Open the files tab at the top.

4. Open the `serverconfig.xml` file in the file editor.

5. Update the server settings:

```xml
<!-- Set the value to false -->
<property name="EACEnabled" value="false"/>
```

6. Click the save button in the bottom left corner.

7. Upload mods using one of the following methods:

::::details File manager
1. Open the files tab at the top.

2. Open the `Mods` folder in the file manager.

3. Click the upload button in the bottom left corner.

4. Select the mods files from your device.

:::tip
You can find mods on [NexusMods](https://www.nexusmods.com/games/7daystodie) or [7D2DMods](https://7daystodiemods.com/).
:::

5. Click the upload button in the bottom right corner.

6. Unzip the archives using the extract button in the actions column.
::::

8. Open the overview tab at the top.

9. Click the restart button in the control block.


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
   min-width: 165px; 
}

table th:nth-child(2) { 
   min-width: 90px; 
}

table th:nth-child(3) { 
   min-width: 150px; 
}

table th:nth-child(4) { 
   min-width: 300px; 
}
</style>