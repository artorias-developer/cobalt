# RimWorld

This tutorial explains how to set up a RimWorld server in the **Cobalt** dashboard.

## Changing configs

1. Open the servers page.

2. Find the server you want to change settings in the table and click the first button in the actions column.

3. Open the files tab at the top.

   ---

   ### `ActionConfig.json`

   1. Open the `Configs/ActionConfig.json` file in the file editor.

   2. Update the settings.

   :::details List of settings
   
   This table refers to version `26.6.23.1`. Some settings may not be available in earlier versions.
   
   | Key                                              | Type    | Default     | Description                                                                                              |
   |--------------------------------------------------|---------|-------------|----------------------------------------------------------------------------------------------------------|
   | `EnableCustomScenarios`                          | boolean | `true`      | Allows players to select custom scenarios.                                                               |
   | `WorldObjectAction.IsEnabled`                    | boolean | `false`     | Enables the creation/interaction with world objects.                                                     |
   | `WorldObjectAction.Cooldown`                     | number  | `250.0`     | Cooldown between world object actions, in milliseconds.                                                  |
   | `PollutionAction.IsEnabled`                      | boolean | `false`     | Allows players with the Biotech DLC installed to spread pollution to all tiles, impacting other players. |
   | `PollutionAction.Cooldown`                       | number  | `300000.0`  | Cooldown between pollution spread actions, in milliseconds.                                              |
   | `RaidAction.IsEnabled`                           | boolean | `true`      | Enables offline visiting and raiding.                                                                    |
   | `RaidAction.Cooldown`                            | number  | `250.0`     | Cooldown between raid actions, in milliseconds.                                                          |
   | `ZoomAction.IsEnabled`                           | boolean | `true`      | Enables zooming in on other players' maps/sites.                                                         |
   | `ZoomAction.Cooldown`                            | number  | `250.0`     | Cooldown between zoom actions, in milliseconds.                                                          |
   | `EventAction.IsEnabled`                          | boolean | `true`      | Enables sending player-triggered events to other players.                                                |
   | `EventAction.Cooldown`                           | number  | `300000.0`  | Cooldown between receiving player-sent events, in milliseconds.                                          |
   | `AidAction.IsEnabled`                            | boolean | `true`      | Enables the transfer of pawns (sending aid) between players.                                             |
   | `AidAction.Cooldown`                             | number  | `250.0`     | Cooldown between receiving player-sent aid, in milliseconds.                                             |
   | `MarketAction.IsEnabled`                         | boolean | `true`      | Enables the in-game market/trading hub.                                                                  |
   | `MarketAction.Cooldown`                          | number  | `250.0`     | Cooldown between market actions, in milliseconds.                                                        |
   | `MarketAction.MinimumPrice`                      | integer | `25`        | Minimum allowed price for an item listed on the market.                                                  |
   | `MarketAction.PriceMultiplier`                   | number  | `0.2`       | Multiplier applied to market item prices.                                                                |
   | `GuildAction.IsEnabled`                          | boolean | `true`      | Enables the creation of user-made factions (guilds).                                                     |
   | `GuildAction.Cooldown`                           | number  | `250.0`     | Cooldown between guild actions, in milliseconds.                                                         |
   | `TradingAction.IsEnabled`                        | boolean | `true`      | Enables the transfer of items between players.                                                           |
   | `TradingAction.Cooldown`                         | number  | `250.0`     | Cooldown between receiving player-sent trades, in milliseconds.                                          |
   | `LeaderboardAction.IsEnabled`                    | boolean | `true`      | Enables the server leaderboard.                                                                          |
   | `LeaderboardAction.Cooldown`                     | number  | `250.0`     | Cooldown between leaderboard actions, in milliseconds.                                                   |
   | `CaravanAction.IsEnabled`                        | boolean | `true`      | Enables sending/receiving caravans between players.                                                      |
   | `CaravanAction.Cooldown`                         | number  | `250.0`     | Cooldown between caravan actions, in milliseconds.                                                       |
   | `SiteAction.IsEnabled`                           | boolean | `true`      | Enables the creation of sites.                                                                           |
   | `SiteAction.Cooldown`                            | number  | `250.0`     | Cooldown between site actions, in milliseconds.                                                          |
   | `SiteAction.TimeInterval`                        | number  | `1800000.0` | Time interval between new sites becoming available, in milliseconds.                                     |
   | `SiteAction.BuildingCost`                        | integer | `3000`      | Cost (in silver) to build a site.                                                                        |
   | `SiteAction.RewardsCount`                        | integer | `100`       | Number of possible rewards available from a site.                                                        |
   | `RoadAction.IsEnabled`                           | boolean | `true`      | Enables the creation of user-built roads.                                                                |
   | `RoadAction.Cooldown`                            | number  | `250.0`     | Cooldown between road actions, in milliseconds.                                                          |
   | `RoadAction.RoadValues.AllowDirtPath`            | boolean | `true`      | Allows building dirt paths.                                                                              |
   | `RoadAction.RoadValues.AllowDirtRoad`            | boolean | `true`      | Allows building dirt roads.                                                                              |
   | `RoadAction.RoadValues.AllowStoneRoad`           | boolean | `true`      | Allows building stone roads.                                                                             |
   | `RoadAction.RoadValues.AllowAsphaltPath`         | boolean | `true`      | Allows building asphalt paths.                                                                           |
   | `RoadAction.RoadValues.AllowAsphaltHighway`      | boolean | `true`      | Allows building asphalt highways.                                                                        |
   | `RoadAction.RoadValues.DirtPathCost`             | integer | `10`        | Cost (in silver) to build a dirt path.                                                                   |
   | `RoadAction.RoadValues.DirtRoadCost`             | integer | `20`        | Cost (in silver) to build a dirt road.                                                                   |
   | `RoadAction.RoadValues.StoneRoadCost`            | integer | `25`        | Cost (in silver) to build a stone road.                                                                  |
   | `RoadAction.RoadValues.AsphaltPathCost`          | integer | `30`        | Cost (in silver) to build an asphalt path.                                                               |
   | `RoadAction.RoadValues.AsphaltHighwayCost`       | integer | `50`        | Cost (in silver) to build an asphalt highway.                                                            |
   | `RoadAction.RoadValues.DirtPathMultiplier`       | number  | `0.45`      | Movement speed multiplier on dirt paths.                                                                 |
   | `RoadAction.RoadValues.DirtRoadMultiplier`       | number  | `0.4`       | Movement speed multiplier on dirt roads.                                                                 |
   | `RoadAction.RoadValues.StoneRoadMultiplier`      | number  | `0.3`       | Movement speed multiplier on stone roads.                                                                |
   | `RoadAction.RoadValues.AsphaltPathMultiplier`    | number  | `0.2`       | Movement speed multiplier on asphalt paths.                                                              |
   | `RoadAction.RoadValues.AsphaltHighwayMultiplier` | number  | `0.1`       | Movement speed multiplier on asphalt highways.                                                           |
   :::

   3. Click the save button in the bottom left corner.

   ---

   ### `BackupConfig.json`

   1. Open the `Configs/BackupConfig.json` file in the file editor.

   2. Update the settings.

   :::details List of settings
   
   This table refers to version `26.6.23.1`. Some settings may not be available in earlier versions.
   
   | Key                 | Type    | Default | Description                                                                                           |
   |---------------------|---------|---------|-------------------------------------------------------------------------------------------------------|
   | `AutomaticBackups`  | boolean | `true`  | Enables this system.                                                                                  |
   | `IntervalHours`     | number  | `24.0`  | Amount of hours in between backups. Keep in mind a backup is generated at every launch of the server. |
   | `AutomaticDeletion` | boolean | `true`  | Removes old backups.                                                                                  |
   | `Amount`            | integer | `3`     | Maximum amount of backups before automatic deletion.                                                  |
   :::

    3. Click the save button in the bottom left corner.

   ---

   ### `ChatConfig.json`

   1. Open the `Configs/ChatConfig.json` file in the file editor.

   2. Update the settings.

   :::details List of settings
   
   This table refers to version `26.6.23.1`. Some settings may not be available in earlier versions.
   
   | Key                       | Type    | Default                   | Description                                         |
   |---------------------------|---------|---------------------------|-----------------------------------------------------|
   | `EnableMoTD`              | boolean | `false`                   | Sends a welcome message to all players that log in. |
   | `MessageOfTheDay`         | string  | `Remember to drink water` | Message sent.                                       |
   | `LoginNotifications`      | boolean | `false`                   | Sends a message when a user logs in.                |
   | `DisconnectNotifications` | boolean | `false`                   | Sends a message when a user logs off.               |
   :::

    3. Click the save button in the bottom left corner.

   ---

   ### `ScenarioConfig.json`

   1. Open the `Configs/ScenarioConfig.json` file in the file editor.

   2. Update the settings.

   :::details List of settings
   
   This table refers to version `26.6.23.1`. Some settings may not be available in earlier versions.

   | Key          | Type    | Default       | Description                                                                             |
   |--------------|---------|---------------|-----------------------------------------------------------------------------------------|
   | `IsEnforced` | boolean | `true`        | Whether a specific scenario is enforced on the server. Configurable at server creation. |
   | `Name`       | string  | `Crashlanded` | Name of the enforced scenario.                                                          |
   :::

    3. Click the save button in the bottom left corner.

   ---

   ### `ServerConfig.json`

   1. Open the `Configs/ServerConfig.json` file in the file editor.

   2. Update the settings.

   :::details List of settings
   
   This table refers to version `26.6.23.1`. Some settings may not be available in earlier versions. Cobalt overrides some default values when a server is created.

   | Key                     | Type    | Default                    | Description                                                                   |
   |-------------------------|---------|----------------------------|-------------------------------------------------------------------------------|
   | `Name`                  | string  | `RimWorld Together Server` | The name of your server. Max of 40 characters.                                |
   | `Description`           | string  | _(blank)_                  | The description of your server. Max of 200 characters.                        |
   | `DiscordURL`            | string  | _(blank)_                  | Link to your server's Discord, shown to players.                              |
   | `SteamWorkshopURL`      | string  | _(blank)_                  | Link to your server's Steam Workshop collection, shown to players.            |
   | `IP`                    | string  | `0.0.0.0`                  | The local network interface you want to bind to.                              |
   | `Port`                  | integer | `25555`                    | The local port you want to bind to.                                           |
   | `MaxPlayers`            | integer | `100`                      | The maximum amount of players that can connect at once.                       |
   | `Verbosity`             | integer | `0`                        | Logging verbosity level. Higher values produce more detailed logs.            |
   | `DisplayChatInConsole`  | boolean | `false`                    | Displays in-game chat messages in the server console.                         |
   | `UseUPnP`               | boolean | `false`                    | Enables your server to use UPnP if your router supports it.                   |
   | `SyncLocalSave`         | boolean | `true`                     | If `true`, the server will not check if the save was modified between logins. |
   | `EnableServerBrowser`   | boolean | `true`                     | Allows your server to be visible on the in-game server browser.               |
   | `EnableServerTelemetry` | boolean | `true`                     | Sends server telemetry/usage data.                                            |
   :::

   :::warning
   Do not change the `IP` and `Port` settings.
   :::

    3. Click the save button in the bottom left corner.

   ---

4. Open the overview tab at the top.

5. Click the restart button in the control block.

## Adding mods

The first time you log in to the game, you'll be appointed as an admin and will be able to choose which mods to enable on the server.

