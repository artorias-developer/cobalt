# Don't Starve Together

This tutorial explains how to set up a Don't Starve Together server in the Cobalt dashboard.

## Adding a token

Immediately after creating the server, you will see the message `No auth token could be found` in the console. This token is used to enable the server to function and to display it in the game's search results.

:::warning
This step is required since you won't be able to connect to the server without token.
:::

1. [Log in](https://accounts.klei.com/login) to your Klei account.

2. Go to the [Don't Starve Together](https://accounts.klei.com/account/game/servers?game=DontStarveTogether) servers section.

3. Create a new server and copy its token.

4. Go to the Cobalt dashboard.

5. Open the servers page.

6. Find the server you want to add token in the table and click the first button in the actions column.

7. Open the files tab at the top.

8. Open the `DoNotStarveTogether/cluster/cluster_token.txt` file in the file editor.

9. Insert the token.

10. Click the save button in the bottom left corner.

11. Open the overview tab at the top.

12. Click the restart button in the control block.

## Changing configs

1. Open the servers page.

2. Find the server you want to change settings in the table and click the first button in the actions column.

3. Open the files tab at the top.

   ---

   ### `cluster.ini`

   1. Open the `DoNotStarveTogether/cluster/cluster.ini` file in the file editor.

   2. Update the settings.

   :::details List of settings
   
   This table refers to version `23922253`. Some settings may not be available in earlier versions. Cobalt overrides some default values when a server is created.
   
   | Key                       | Type    | Default       | Description                                                                                                                                                                                                                                                                             |
   |---------------------------|---------|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
   | `max_players`             | integer | `16`          | The maximum number of players that may be connected to the cluster at one time.                                                                                                                                                                                                         |
   | `pvp`                     | boolean | `false`       | Enables PVP.<br>`true` - enabled<br>`false` - disabled                                                                                                                                                                                                                                  |
   | `game_mode`               | string  | `survival`    | The cluster's game mode: `survival`, `endless`, `wilderness`.                                                                                                                                                                                                                           |
   | `pause_when_empty`        | boolean | `false`       | Pauses the server when there are no players connected.<br>`true` - enabled<br>`false` - disabled                                                                                                                                                                                        |
   | `vote_enabled`            | boolean | `true`        | Enables voting features.<br>`true` - enabled<br>`false` - disabled                                                                                                                                                                                                                      |
   | `offline_cluster`         | boolean | `false`       | Creates an offline cluster. The server will not be listed publicly, only LAN players can join, and steam-related functionality will not work.<br>`true` - enabled<br>`false` - disabled                                                                                                 |
   | `tick_rate`               | integer | `15`          | Number of times per second the server sends updates to clients. Increasing this may improve precision but increases network traffic. Recommended to leave at default; if changed, use only for LAN games with a number evenly divisible into 60 (`15`, `20`, `30`).                     |
   | `whitelist_slots`         | integer | `0`           | Number of reserved slots for whitelisted players. To whitelist a player, add their Klei UserId to `whitelist.txt` in the same directory as `cluster.ini`.                                                                                                                               |
   | `cluster_password`        | string  | _(blank)_     | Password that players must enter to join the server. Leave blank or omit for no password.                                                                                                                                                                                               |
   | `cluster_name`            | string  | `DST Server`  | The name for the server cluster. This is the name shown in the server browser.                                                                                                                                                                                                          |
   | `cluster_description`     | string  | _(blank)_     | Cluster description. Shown in the server details area on the "Browse Games" screen.                                                                                                                                                                                                     |
   | `lan_only_cluster`        | boolean | `false`       | When set to `true`, the server will only accept connections from machines on the same LAN.<br>`true` - enabled<br>`false` - disabled                                                                                                                                                    |
   | `cluster_intention`       | string  | `cooperative` | The cluster's playstyle: `cooperative`, `competitive`, `social`, `madness`.                                                                                                                                                                                                             |
   | `autosaver_enabled`       | boolean | `true`        | When set to `false`, the game will no longer automatically save at the end of each day. The game still saves on shutdown, and can be saved manually with `c_save()`.<br>`true` - enabled<br>`false` - disabled                                                                          |
   | `max_snapshots`           | integer | `6`           | Maximum number of snapshots to retain. Created every time a save occurs, available in the "Rollback" tab on the "Host Game" screen.                                                                                                                                                     |
   | `console_enabled`         | boolean | `true`        | Allows lua commands to be entered in the command prompt or terminal the server is running in.<br>`true` - enabled<br>`false` - disabled                                                                                                                                                 |
   | `shard_enabled`           | boolean | `false`       | Enables server sharding. Must be `true` for multi-level servers; can be omitted for single-level servers.<br>`true` - enabled<br>`false` - disabled                                                                                                                                     |
   | `bind_ip`                 | string  | `127.0.0.1`   | Network address the master server listens on for other shard servers to connect to. Use `127.0.0.1` if all servers are on the same machine, or `0.0.0.0` if on different machines/containers. Only needed for the master server. Required if `shard_enabled=true` and `is_master=true`. |
   | `master_ip`               | string  | _(blank)_     | IP address a non-master shard uses to connect to the master shard. Use `127.0.0.1` if all servers are on the same machine, or `cobalt_server_<server_id>` if in different containers. Required if `shard_enabled=true` and `is_master=false`.                                           |
   | `master_port`             | integer | `10888`       | UDP port the master server listens on, and that non-master shards use to connect to it. Should be the same for all shards (set once in `cluster.ini`), and must differ from `server_port` on any shard running on the same machine as the master.                                       |
   | `cluster_key`             | string  | _(blank)_     | Password used to authenticate a slave server to the master. Must match across machines/containers that need to connect to each other. Required if `shard_enabled=true`.                                                                                                                 |
   | `steam_group_only`        | boolean | `false`       | When set to `true`, the server only allows connections from players belonging to the steam group listed in `steam_group_id`.<br>`true` - enabled<br>`false` - disabled                                                                                                                  |
   | `steam_group_id`          | integer | `0`           | Steam group ID for `steam_group_only` / `steam_group_admins` settings.                                                                                                                                                                                                                  |
   | `steam_group_admins`      | boolean | `false`       | When set to `true`, admins of the steam group specified in `steam_group_id` also have admin status on the server.<br>`true` - enabled<br>`false` - disabled                                                                                                                             |
   :::

   :::warning
   Do not change the `bind_ip` and `master_port` settings.
   :::

   3. Click the save button in the bottom left corner.

   ---

   ### `server.ini`

   1. Open the `DoNotStarveTogether/cluster/Main/server.ini` file in the file editor.

   2. Update the settings.

   :::details List of settings
   
   This table refers to version `23922253`. Some settings may not be available in earlier versions. Cobalt overrides some default values when a server is created.   

   | Key                   | Type    | Default                | Description                                                                                                                                                                                                                                                                                                                                                                 |
   |-----------------------|---------|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
   | `server_port`         | integer | `10999`                | The UDP port that this server will listen for connections on. If running a multi-level cluster, this port must be different for each server on the same machine or container. Must be between `10998` and `11018` inclusive for players on the same LAN to see it in their server listing. Ports below `1024` are restricted to privileged users on some operating systems. |
   | `is_master`           | boolean | _(blank)_              | Sets a shard to be the master shard for a cluster. There must be exactly one master server per cluster. Set to `true` in the master server's `server.ini`, and `false` in every other `server.ini`. Required if `shard_enabled=true`.<br>`true` - master<br>`false` - not master                                                                                            |
   | `name`                | string  | _(blank)_              | The name of the shard that will show up in log files. Ignored for the master server, which always has the name `[SHDMASTER]`.                                                                                                                                                                                                                                               |
   | `id`                  | integer | _(randomly generated)_ | Automatically generated for non-master servers, used internally to uniquely identify a server. Altering or removing this may cause problems on your server if anybody's character currently resides in the world that this server manages.                                                                                                                                  |
   | `authentication_port` | integer | `8766`                 | Internal port used by steam. Must be different for each server running on the same machine or container.                                                                                                                                                                                                                                                                    |
   | `master_server_port`  | integer | `27016`                | Internal port used by steam. Must be different for each server running on the same machine or container.                                                                                                                                                                                                                                                                    |
   :::

   :::warning
   Do not change the `id`, `server_port`, `authentication_port` and `master_server_port` settings.
   :::

   3. Click the save button in the bottom left corner.

   ---

   ### `worldgenoverride.lua`

   1. Open the `DoNotStarveTogether/cluster/Main` folder in the file manager.
   
   2. Rename the file if you haven't already:
      
      - `worldgenoverride.forest.lua` to `worldgenoverride.lua` for the `Forest` server.
      - `worldgenoverride.caves.lua` to `worldgenoverride.lua` for the `Caves` server.
   
   3. Open the renamed `worldgenoverride.lua` file in the file editor.

   4. Update the settings.

   :::details List of Forest settings

   This table refers to version `23922253`. Some settings may not be available in earlier versions.

   | Key                                  | Type    | Default           | Description                                                                                                                                      |
   |--------------------------------------|---------|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
   | `alternatehunt`                      | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `angrybees`                          | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `antliontribute`                     | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `autumn`                             | string  | `default`         | Available values: `noseason`, `veryshortseason`, `shortseason`, `default`, `longseason`, `verylongseason`, `random`.                             |
   | `balatro`                            | string  | `default`         |                                                                                                                                                  |
   | `bananabush_portalrate`              | string  | `default`         |                                                                                                                                                  |
   | `basicresource_regrowth`             | string  | `none`            |                                                                                                                                                  |
   | `bats_setting`                       | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `bearger`                            | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `beefalo`                            | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `beefaloheat`                        | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `beequeen`                           | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `bees`                               | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `bees_setting`                       | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `berrybush`                          | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `birds`                              | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `boons`                              | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `branching`                          | string  | `default`         | Available values: `never`, `least`, `default`, `most`, `random`.                                                                                 |
   | `brightmarecreatures`                | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `bunnymen_setting`                   | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `butterfly`                          | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `buzzard`                            | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `cactus`                             | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `cactus_regrowth`                    | string  | `default`         |                                                                                                                                                  |
   | `carrot`                             | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `carrots_regrowth`                   | string  | `default`         | Available values: `never`, `veryslow`, `slow`, `default`, `fast`, `veryfast`.                                                                    |
   | `catcoon`                            | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `catcoons`                           | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `chess`                              | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `cookiecutters`                      | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `crabking`                           | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `crow_carnival`                      | string  | `default`         | Available values: `default`, `enabled`.                                                                                                          |
   | `darkness`                           | string  | `default`         |                                                                                                                                                  |
   | `day`                                | string  | `default`         | Available values: `default`, `longday`, `longdusk`, `longnight`, `noday`, `nodusk`, `nonight`, `onlyday`, `onlydusk`, `onlynight`.               |
   | `daywalker2`                         | string  | `default`         |                                                                                                                                                  |
   | `deciduousmonster`                   | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `deciduoustree_regrowth`             | string  | `default`         | Available values: `never`, `veryslow`, `slow`, `default`, `fast`, `veryfast`.                                                                    |
   | `deerclops`                          | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `dragonfly`                          | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `dropeverythingondespawn`            | string  | `default`         | Available values: `default`, `always`.                                                                                                           |
   | `evergreen_regrowth`                 | string  | `default`         | Available values: `never`, `veryslow`, `slow`, `default`, `fast`, `veryfast`.                                                                    |
   | `extrastartingitems`                 | string  | `default`         | Available values: `0`, `5`, `default`, `15`, `20`, `none`.                                                                                       |
   | `eyeofterror`                        | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `fishschools`                        | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `flint`                              | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `flowers`                            | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `flowers_regrowth`                   | string  | `default`         | Available values: `never`, `veryslow`, `slow`, `default`, `fast`, `veryfast`.                                                                    |
   | `frograin`                           | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `frogs`                              | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `fruitfly`                           | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `ghostenabled`                       | string  | `always`          |                                                                                                                                                  |
   | `ghostsanitydrain`                   | string  | `always`          |                                                                                                                                                  |
   | `gnarwail`                           | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `goosemoose`                         | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `grass`                              | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `grassgekkos`                        | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `hallowed_nights`                    | string  | `default`         | Available values: `default`, `enabled`.                                                                                                          |
   | `has_ocean`                          | boolean | `true`            |                                                                                                                                                  |
   | `healthpenalty`                      | string  | `always`          |                                                                                                                                                  |
   | `hound_mounds`                       | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `houndmound`                         | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `hounds`                             | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `hunger`                             | string  | `default`         |                                                                                                                                                  |
   | `hunt`                               | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `junkyard`                           | string  | `default`         |                                                                                                                                                  |
   | `keep_disconnected_tiles`            | boolean | `true`            |                                                                                                                                                  |
   | `klaus`                              | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `krampus`                            | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `layout_mode`                        | string  | `LinkNodesByKeys` |                                                                                                                                                  |
   | `lessdamagetaken`                    | string  | `none`            |                                                                                                                                                  |
   | `liefs`                              | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `lightcrab_portalrate`               | string  | `default`         |                                                                                                                                                  |
   | `lightning`                          | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `lightninggoat`                      | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `loop`                               | string  | `default`         | Available values: `never`, `default`, `always`.                                                                                                  |
   | `lunarhail_frequency`                | string  | `default`         |                                                                                                                                                  |
   | `lureplants`                         | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `malbatross`                         | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `marshbush`                          | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `merm`                               | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `merms`                              | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `meteorshowers`                      | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `meteorspawner`                      | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `moles`                              | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `moles_setting`                      | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `monkeytail_portalrate`              | string  | `default`         |                                                                                                                                                  |
   | `moon_berrybush`                     | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `moon_bullkelp`                      | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `moon_carrot`                        | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `moon_fissure`                       | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `moon_fruitdragon`                   | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `moon_hotspring`                     | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `moon_rock`                          | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `moon_sapling`                       | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `moon_spider`                        | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `moon_spiders`                       | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `moon_starfish`                      | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `moon_tree`                          | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `moon_tree_regrowth`                 | string  | `default`         | Available values: `never`, `veryslow`, `slow`, `default`, `fast`, `veryfast`.                                                                    |
   | `mosquitos`                          | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `mushroom`                           | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `mutated_bearger`                    | string  | `default`         |                                                                                                                                                  |
   | `mutated_bird_gestalt`               | string  | `default`         |                                                                                                                                                  |
   | `mutated_birds`                      | string  | `default`         |                                                                                                                                                  |
   | `mutated_buzzard_gestalt`            | string  | `default`         |                                                                                                                                                  |
   | `mutated_deerclops`                  | string  | `default`         |                                                                                                                                                  |
   | `mutated_hounds`                     | string  | `default`         | Available values: `never`, `default`.                                                                                                            |
   | `mutated_merm`                       | string  | `default`         |                                                                                                                                                  |
   | `mutated_spiderqueen`                | string  | `default`         |                                                                                                                                                  |
   | `mutated_warg`                       | string  | `default`         |                                                                                                                                                  |
   | `no_joining_islands`                 | boolean | `true`            |                                                                                                                                                  |
   | `no_wormholes_to_disconnected_tiles` | boolean | `true`            |                                                                                                                                                  |
   | `ocean_bullkelp`                     | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `ocean_otterdens`                    | string  | `default`         |                                                                                                                                                  |
   | `ocean_seastack`                     | string  | `ocean_default`   | Available values: `ocean_never`, `ocean_rare`, `ocean_uncommon`, `ocean_default`, `ocean_often`, `ocean_mostly`, `ocean_always`, `ocean_insane`. |
   | `ocean_shoal`                        | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `ocean_waterplant`                   | string  | `ocean_default`   | Available values: `ocean_never`, `ocean_rare`, `ocean_uncommon`, `ocean_default`, `ocean_often`, `ocean_mostly`, `ocean_always`, `ocean_insane`. |
   | `ocean_wobsterden`                   | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `otters_setting`                     | string  | `default`         |                                                                                                                                                  |
   | `palmcone_seed_portalrate`           | string  | `default`         |                                                                                                                                                  |
   | `palmconetree`                       | string  | `default`         |                                                                                                                                                  |
   | `palmconetree_regrowth`              | string  | `default`         |                                                                                                                                                  |
   | `penguins`                           | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `penguins_moon`                      | string  | `default`         | Available values: `never`, `default`.                                                                                                            |
   | `perd`                               | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `petrification`                      | string  | `default`         | Available values: `none`, `few`, `default`, `many`, `max`.                                                                                       |
   | `pigs`                               | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `pigs_setting`                       | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `pirateraids`                        | string  | `default`         |                                                                                                                                                  |
   | `ponds`                              | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `portal_spawnrate`                   | string  | `default`         |                                                                                                                                                  |
   | `portalresurection`                  | string  | `none`            |                                                                                                                                                  |
   | `powder_monkey_portalrate`           | string  | `default`         |                                                                                                                                                  |
   | `prefabswaps_start`                  | string  | `default`         | Available values: `classic`, `default`, `highly random`.                                                                                         |
   | `rabbits`                            | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `rabbits_setting`                    | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `reeds`                              | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `reeds_regrowth`                     | string  | `default`         |                                                                                                                                                  |
   | `regrowth`                           | string  | `default`         | Available values: `never`, `veryslow`, `slow`, `default`, `fast`, `veryfast`.                                                                    |
   | `resettime`                          | string  | `default`         |                                                                                                                                                  |
   | `rifts_enabled`                      | string  | `default`         |                                                                                                                                                  |
   | `rifts_frequency`                    | string  | `default`         |                                                                                                                                                  |
   | `roads`                              | string  | `default`         | Available values: `never`, `default`.                                                                                                            |
   | `rock`                               | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `rock_ice`                           | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `saltstack_regrowth`                 | string  | `default`         | Available values: `never`, `veryslow`, `slow`, `default`, `fast`, `veryfast`.                                                                    |
   | `sapling`                            | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `season_start`                       | string  | `default`         | Available values: `default`, `winter`, `spring`, `summer`, `autumn\|spring`, `winter\|summer`, `autumn\|winter\|spring\|summer`.                 |                          |
   | `seasonalstartingitems`              | string  | `default`         | Available values: `never`, `default`.                                                                                                            |
   | `shadowcreatures`                    | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `sharkboi`                           | string  | `default`         |                                                                                                                                                  |
   | `sharks`                             | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `spawnmode`                          | string  | `fixed`           |                                                                                                                                                  |
   | `spawnprotection`                    | string  | `default`         | Available values: `never`, `default`, `always`.                                                                                                  |
   | `specialevent`                       | string  | `default`         | Available values: `none`, `default`.                                                                                                             |
   | `spider_warriors`                    | string  | `default`         | Available values: `never`, `default`.                                                                                                            |
   | `spiderqueen`                        | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `spiders`                            | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `spiders_setting`                    | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `spring`                             | string  | `default`         | Available values: `noseason`, `veryshortseason`, `shortseason`, `default`, `longseason`, `verylongseason`, `random`.                             |
   | `squid`                              | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `stageplays`                         | string  | `default`         |                                                                                                                                                  |
   | `start_location`                     | string  | `default`         | Available values: `lavaarena`, `plus`, `darkness`, `quagmire_startlocation`, `caves`, `default`.                                                 |
   | `summer`                             | string  | `default`         | Available values: `noseason`, `veryshortseason`, `shortseason`, `default`, `longseason`, `verylongseason`, `random`.                             |
   | `summerhounds`                       | string  | `default`         | Available values: `never`, `default`.                                                                                                            |
   | `tallbirds`                          | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `task_set`                           | string  | `default`         | Available values: `default`, `cave_default`, `quagmire_taskset`, `classic`, `lavaarena_taskset`.                                                 |
   | `temperaturedamage`                  | string  | `default`         |                                                                                                                                                  |
   | `tentacles`                          | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `terrariumchest`                     | string  | `default`         | Available values: `never`, `default`.                                                                                                            |
   | `touchstone`                         | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `trees`                              | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `tumbleweed`                         | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `twiggytrees_regrowth`               | string  | `default`         | Available values: `never`, `veryslow`, `slow`, `default`, `fast`, `veryfast`.                                                                    |
   | `walrus`                             | string  | `default`         | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                                 |
   | `walrus_setting`                     | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `wanderingtrader_enabled`            | string  | `always`          |                                                                                                                                                  |
   | `wasps`                              | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `weather`                            | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `wildfires`                          | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `winter`                             | string  | `default`         | Available values: `noseason`, `veryshortseason`, `shortseason`, `default`, `longseason`, `verylongseason`, `random`.                             |
   | `winterhounds`                       | string  | `default`         | Available values: `never`, `default`.                                                                                                            |
   | `winters_feast`                      | string  | `default`         | Available values: `default`, `enabled`.                                                                                                          |
   | `wobsters`                           | string  | `default`         | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                                 |
   | `world_size`                         | string  | `default`         | Available values: `small`, `medium`, `default`, `huge`.                                                                                          |
   | `wormhole_prefab`                    | string  | `wormhole`        |                                                                                                                                                  |
   | `year_of_the_beefalo`                | string  | `default`         | Available values: `default`, `enabled`.                                                                                                          |
   | `year_of_the_bunnyman`               | string  | `default`         | Available values: `default`, `enabled`.                                                                                                          |
   | `year_of_the_carrat`                 | string  | `default`         | Available values: `default`, `enabled`.                                                                                                          |
   | `year_of_the_catcoon`                | string  | `default`         | Available values: `default`, `enabled`.                                                                                                          |
   | `year_of_the_dragonfly`              | string  | `default`         | Available values: `default`, `enabled`.                                                                                                          |
   | `year_of_the_gobbler`                | string  | `default`         | Available values: `default`, `enabled`.                                                                                                          |
   | `year_of_the_knight`                 | string  | `default`         | Available values: `default`, `enabled`.                                                                                                          |
   | `year_of_the_pig`                    | string  | `default`         | Available values: `default`, `enabled`.                                                                                                          |
   | `year_of_the_snake`                  | string  | `default`         | Available values: `default`, `enabled`.                                                                                                          |
   | `year_of_the_varg`                   | string  | `default`         | Available values: `default`, `enabled`.                                                                                                          |
   :::
 
   :::details List of Caves settings

   This table refers to version `23922253`. Some settings may not be available in earlier versions.

   | Key                          | Type   | Default              | Description                                                                                                                        |
   |------------------------------|--------|----------------------|------------------------------------------------------------------------------------------------------------------------------------|
   | `acidrain_enabled`           | string | `always`             |                                                                                                                                    |
   | `atriumgate`                 | string | `default`            | Available values: `veryslow`, `slow`, `default`, `fast`, `veryfast`.                                                               |
   | `banana`                     | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `basicresource_regrowth`     | string | `none`               |                                                                                                                                    |
   | `bats`                       | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `bats_setting`               | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `beefaloheat`                | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `berrybush`                  | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `boons`                      | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `branching`                  | string | `default`            | Available values: `never`, `least`, `default`, `most`, `random`.                                                                   |
   | `brightmarecreatures`        | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `bunnymen`                   | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `bunnymen_setting`           | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `cave_ponds`                 | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `cave_spiders`               | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `cavelight`                  | string | `default`            | Available values: `never`, `veryslow`, `slow`, `default`, `fast`, `veryfast`.                                                      |
   | `chess`                      | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `chest_mimics`               | string | `default`            |                                                                                                                                    |
   | `crow_carnival`              | string | `default`            | Available values: `default`, `enabled`.                                                                                            |
   | `darkness`                   | string | `default`            |                                                                                                                                    |
   | `day`                        | string | `default`            | Available values: `default`, `longday`, `longdusk`, `longnight`, `noday`, `nodusk`, `nonight`, `onlyday`, `onlydusk`, `onlynight`. |
   | `daywalker`                  | string | `default`            |                                                                                                                                    |
   | `dropeverythingondespawn`    | string | `default`            | Available values: `default`, `always`.                                                                                             |
   | `dustmoths`                  | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `earthquakes`                | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `evergreen_regrowth`         | string | `default`            | Available values: `never`, `veryslow`, `slow`, `default`, `fast`, `veryfast`.                                                      |
   | `extrastartingitems`         | string | `default`            | Available values: `0`, `5`, `default`, `15`, `20`, `none`.                                                                         |
   | `fern`                       | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `fissure`                    | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `flint`                      | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `flower_cave`                | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `flower_cave_regrowth`       | string | `default`            |                                                                                                                                    |
   | `fruitfly`                   | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `ghostenabled`               | string | `always`             |                                                                                                                                    |
   | `ghostsanitydrain`           | string | `always`             |                                                                                                                                    |
   | `grass`                      | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `grassgekkos`                | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `hallowed_nights`            | string | `default`            | Available values: `default`, `enabled`.                                                                                            |
   | `healthpenalty`              | string | `always`             |                                                                                                                                    |
   | `hunger`                     | string | `default`            |                                                                                                                                    |
   | `itemmimics`                 | string | `default`            |                                                                                                                                    |
   | `krampus`                    | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `layout_mode`                | string | `RestrictNodesByKey` |                                                                                                                                    |
   | `lessdamagetaken`            | string | `none`               |                                                                                                                                    |
   | `lichen`                     | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `liefs`                      | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `lightflier_flower_regrowth` | string | `default`            |                                                                                                                                    |
   | `lightfliers`                | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `loop`                       | string | `default`            | Available values: `never`, `default`, `always`.                                                                                    |
   | `marshbush`                  | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `merms`                      | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `molebats`                   | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `moles_setting`              | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `monkey`                     | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `monkey_setting`             | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `moon_spider`                | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `mushgnome`                  | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `mushroom`                   | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `mushtree`                   | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `mushtree_moon_regrowth`     | string | `default`            |                                                                                                                                    |
   | `mushtree_regrowth`          | string | `default`            |                                                                                                                                    |
   | `mutated_birds`              | string | `default`            |                                                                                                                                    |
   | `mutated_merm`               | string | `default`            |                                                                                                                                    |
   | `mutated_spiderqueen`        | string | `default`            |                                                                                                                                    |
   | `nightmarecreatures`         | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `pigs_setting`               | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `portalresurection`          | string | `none`               |                                                                                                                                    |
   | `prefabswaps_start`          | string | `default`            | Available values: `classic`, `default`, `highly random`.                                                                           |
   | `reeds`                      | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `reeds_regrowth`             | string | `default`            |                                                                                                                                    |
   | `regrowth`                   | string | `default`            | Available values: `never`, `veryslow`, `slow`, `default`, `fast`, `veryfast`.                                                      |
   | `resettime`                  | string | `default`            |                                                                                                                                    |
   | `rifts_enabled_cave`         | string | `default`            |                                                                                                                                    |
   | `rifts_frequency_cave`       | string | `default`            |                                                                                                                                    |
   | `roads`                      | string | `never`              | Available values: `never`, `default`.                                                                                              |
   | `rock`                       | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `rocky`                      | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `rocky_setting`              | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `sapling`                    | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `season_start`               | string | `default`            | Available values: `default`, `winter`, `spring`, `summer`, `autumn\|spring`, `winter\|summer`, `autumn\|winter\|spring\|summer`.   |
   | `seasonalstartingitems`      | string | `default`            | Available values: `never`, `default`.                                                                                              |
   | `shadowcreatures`            | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `slurper`                    | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `slurtles`                   | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `slurtles_setting`           | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `snurtles`                   | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `spawnmode`                  | string | `fixed`              |                                                                                                                                    |
   | `spawnprotection`            | string | `default`            | Available values: `never`, `default`, `always`.                                                                                    |
   | `specialevent`               | string | `default`            | Available values: `none`, `default`, `hallowed_nights`, `winters_feast`, `year_of_the_gobbler`.                                    |
   | `spider_dropper`             | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `spider_hider`               | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `spider_spitter`             | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `spider_warriors`            | string | `default`            | Available values: `never`, `default`.                                                                                              |
   | `spiderqueen`                | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `spiders`                    | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `spiders_setting`            | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `start_location`             | string | `caves`              | Available values: `lavaarena`, `plus`, `darkness`, `quagmire_startlocation`, `caves`, `default`.                                   |
   | `task_set`                   | string | `cave_default`       | Available values: `default`, `cave_default`, `quagmire_taskset`, `classic`, `lavaarena_taskset`.                                   |
   | `temperaturedamage`          | string | `default`            |                                                                                                                                    |
   | `tentacles`                  | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `toadstool`                  | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `touchstone`                 | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `tree_rock`                  | string | `default`            |                                                                                                                                    |
   | `tree_rock_regrowth`         | string | `default`            |                                                                                                                                    |
   | `trees`                      | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `twiggytrees_regrowth`       | string | `default`            | Available values: `never`, `veryslow`, `slow`, `default`, `fast`, `veryfast`.                                                      |
   | `weather`                    | string | `default`            |                                                                                                                                    |
   | `winters_feast`              | string | `default`            | Available values: `default`, `enabled`.                                                                                            |
   | `world_size`                 | string | `default`            | Available values: `small`, `medium`, `default`, `huge`.                                                                            |
   | `wormattacks`                | string | `default`            | Available values: `never`, `rare`, `default`, `often`, `always`.                                                                   |
   | `wormattacks_boss`           | string | `default`            |                                                                                                                                    |
   | `wormhole_prefab`            | string | `tentacle_pillar`    |                                                                                                                                    |
   | `wormlights`                 | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `worms`                      | string | `default`            | Available values: `never`, `rare`, `uncommon`, `default`, `often`, `mostly`, `always`, `insane`.                                   |
   | `year_of_the_beefalo`        | string | `default`            | Available values: `default`, `enabled`.                                                                                            |
   | `year_of_the_bunnyman`       | string | `default`            | Available values: `default`, `enabled`.                                                                                            |
   | `year_of_the_carrat`         | string | `default`            | Available values: `default`, `enabled`.                                                                                            |
   | `year_of_the_catcoon`        | string | `default`            | Available values: `default`, `enabled`.                                                                                            |
   | `year_of_the_dragonfly`      | string | `default`            | Available values: `default`, `enabled`.                                                                                            |
   | `year_of_the_gobbler`        | string | `default`            | Available values: `default`, `enabled`.                                                                                            |
   | `year_of_the_knight`         | string | `default`            | Available values: `default`, `enabled`.                                                                                            |
   | `year_of_the_pig`            | string | `default`            | Available values: `default`, `enabled`.                                                                                            |
   | `year_of_the_snake`          | string | `default`            | Available values: `default`, `enabled`.                                                                                            |
   | `year_of_the_varg`           | string | `default`            | Available values: `default`, `enabled`.                                                                                            |
   :::

   5. Click the save button in the bottom left corner.

   ---

4. Open the overview tab at the top.

5. Click the restart button in the control block.

## Adding caves

If you want to add caves to your world, follow the instructions below:

1. Open the servers page.

2. Create two servers, [add tokens](#adding-a-token) to each one and stop them.

3. Decide which of the two will be `Forest` and which will be `Caves`.

4. Find the `Forest` server in the table and click the first button in the actions column.

5. Open the files tab at the top.

6. Open the `DoNotStarveTogether/cluster/Main` folder in the file manager.

7. Rename the `worldgenoverride.forest.lua` file to `worldgenoverride.lua` using the rename button in the actions column.

8. Open the `DoNotStarveTogether/cluster/cluster.ini` file in the file editor.

9. Update the cluster settings:

```ini
# Set the value to true
shard_enabled=true

# Remove the # at the beginning
bind_ip=0.0.0.0
```

:::warning
Make sure that `master_ip` setting starts with `#`.
:::

10. Copy the entire contents of the file.

11. Click the save button in the bottom left corner.

12. Go back to the servers page.

13. Find the `Caves` server in the table and click the first button in the actions column.

14. Open the files tab at the top.

15. Open the `DoNotStarveTogether/cluster/cluster.ini` file in the file editor.

16. Delete everything from the file and paste the content of the file from step `10`.

17. Update the cluster settings:

```ini
# Remove the # at the beginning
master_ip=cobalt_server_1

# Add # at the beginning
#bind_ip=0.0.0.0
``` 

:::warning
Do not change the `master_ip` value, the example shows a random value, and yours may be different.
:::

:::warning
Make sure that:

- `shard_enabled` setting is set to `true`.
- `bind_ip` setting starts with `#`.
:::

18. Click the save button in the bottom left corner.

19. Open the `DoNotStarveTogether/cluster/Main/server.ini` file in the file editor.

20. Update the server settings:

```ini
# Set the value to "false"
is_master=false

# Set the value to "Caves"
name=Caves
``` 

21. Click the save button in the bottom left corner.

22. Open the `DoNotStarveTogether/cluster/Main` folder in the file manager.

23. Rename the `worldgenoverride.caves.lua` file to `worldgenoverride.lua` using the rename button in the actions column.

24. Delete the `DoNotStarveTogether/cluster/Main/save` folder using the delete button in the actions column.

25. Start the `Forest` server and wait for it to finish starting up.

26. Start the `Caves` server.

## Adding mods

1. Open the servers page.

2. Find the server you want to add mods in the table and click the first button in the actions column.

3. Open the files tab at the top.

4. Open the `mods/dedicated_server_mods_setup.lua` file in the file editor.

5. Register the IDs of individual mods using `ServerModSetup` or the IDs of mod collections using `ServerModCollectionSetup`:

```lua
# Individual mod
ServerModSetup("350811795")

# Mod collection
ServerModCollectionSetup("379114180")
```

:::tip
You can find mods on [Steam Workshop](https://steamcommunity.com/app/322330/workshop/).

Example: https://steamcommunity.com/sharedfiles/filedetails/?id=350811795

In this case, the ID is `350811795`.
:::

6. Click the save button in the bottom left corner.
   
7. Open the `DoNotStarveTogether/cluster/Main/modoverrides.lua` file in the file editor.

8. Enable mods:

```lua
return {
  ["workshop-375859599"] = { 
    enabled = true 
  },
  ["workshop-3740646188"] = { 
    enabled = true 
  }
}
```

9. Click the save button in the bottom left corner.

10. Open the overview tab at the top.

11. Click the restart button in the control block.

:::warning
If you're playing with `Caves`, you'll need to do the same for the second server.
:::