# Minecraft

This tutorial explains how to set up a Minecraft server in the Cobalt dashboard.

## Changing configs

1. Open the servers page.

2. Find the server you want to change settings in the table and click the first button in the actions column.

3. Open the files tab at the top.
   
   ---
   
   ### `server.properties`
   
   1. Open the `server.properties` file in the file editor.
   
   2. Update the settings.

   :::details List of settings
   
   This table refers to version `26.2`. Some settings may not be available in earlier versions. Cobalt overrides some default values when a server is created.
   
   | Key                                       | Type      | Default              | Description                                                                                                                                       |
   |-------------------------------------------|-----------|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
   | `accepts-transfers`                       | boolean   | `false`              | Whether to accept incoming player transfers via transfer packet.                                                                                  |
   | `allow-flight`                            | boolean   | `false`              | Allows flight in Survival mode if the player has a fly mod. Players in air for 5+ seconds get kicked if disabled.                                 |
   | `broadcast-console-to-ops`                | boolean   | `true`               | Sends console command outputs to all online operators.                                                                                            |
   | `broadcast-rcon-to-ops`                   | boolean   | `true`               | Sends RCON command outputs to all online operators.                                                                                               |
   | `bug-report-link`                         | string    | _(blank)_            | URL for the `report_bug` server link. Not sent if empty.                                                                                          |
   | `chat-spam-threshold-seconds`             | integer   | `10`                 | Ticks before a player is kicked for sending too many chat messages. `0` disables.                                                                 |
   | `command-spam-threshold-seconds`          | integer   | `10`                 | Ticks before a player is kicked for sending too many commands. `0` disables.                                                                      |
   | `difficulty`                              | string    | `easy`               | Server difficulty: `peaceful`, `easy`, `normal`, `hard`.                                                                                          |
   | `enable-code-of-conduct`                  | boolean   | `false`              | Whether to show code of conduct files from the `codeofconduct` folder to players on join.                                                         |
   | `enable-jmx-monitoring`                   | boolean   | `false`              | Exposes a JMX MBean with tick time metrics. Requires additional JVM flags.                                                                        |
   | `enable-query`                            | boolean   | `false`              | Enables GameSpy4 query protocol for server info.                                                                                                  |
   | `enable-rcon`                             | boolean   | `false`              | Enables remote console access via RCON. Not recommended over untrusted networks.                                                                  |
   | `enable-status`                           | boolean   | `true`               | Makes the server appear online in the server list. If `false`, still accepts connections but appears offline.                                     |
   | `enforce-secure-profile`                  | boolean   | `true`               | Requires players to have a Mojang-signed public key. Chat will be unsigned if disabled.                                                           |
   | `enforce-whitelist`                       | boolean   | `false`              | Kicks online players not on the whitelist when it is reloaded.                                                                                    |
   | `entity-broadcast-range-percentage`       | integer   | `100`                | Percentage of default distance at which entities are sent to clients. Lower = less lag, shorter render distance. Must be between `10` and `1000`. |
   | `force-gamemode`                          | boolean   | `false`              | Forces players to join in the default game mode every time.                                                                                       |
   | `function-permission-level`               | integer   | `2`                  | Default permission level for functions. Must be between `1` and `4`.                                                                              |
   | `gamemode`                                | string    | `survival`           | Default game mode: `survival`, `creative`, `adventure`, `spectator`.                                                                              |
   | `generate-structures`                     | boolean   | `true`               | Whether structures like villages are generated. Dungeons still generate if `false`.                                                               |
   | `generator-settings`                      | string    | `{}`                 | JSON settings for custom world generation. Used with `level-type=minecraft:flat`.                                                                 |
   | `hardcore`                                | boolean   | `false`              | Enables hardcore mode - players become spectators on death.                                                                                       |
   | `hide-online-players`                     | boolean   | `false`              | Disables sending the player list in status requests.                                                                                              |
   | `initial-disabled-packs`                  | string    | _(blank)_            | Comma-separated list of datapacks disabled on world creation.                                                                                     |
   | `initial-enabled-packs`                   | string    | `vanilla`            | Comma-separated list of datapacks enabled on world creation. Feature packs must be explicitly listed.                                             |
   | `level-name`                              | string    | `world`              | World name and folder path. Can be absolute or relative.                                                                                          |
   | `level-seed`                              | string    | _(blank)_            | World seed. Random if blank.                                                                                                                      |
   | `level-type`                              | string    | `minecraft:normal`   | World preset: `minecraft:normal`, `minecraft:flat`, `minecraft:large_biomes`, `minecraft:amplified`, `minecraft:single_biome_surface`.            |
   | `log-ips`                                 | boolean   | `true`               | Whether client IPs are shown in console and log output.                                                                                           |
   | `management-server-allowed-origins`       | string    | _(blank)_            | Allowed origins for the Minecraft Server Management Protocol.                                                                                     |
   | `management-server-enabled`               | boolean   | `false`              | Whether the Minecraft Server Management Protocol is enabled.                                                                                      |
   | `management-server-host`                  | string    | `localhost`          | Host the management server listens on.                                                                                                            |
   | `management-server-port`                  | integer   | `0`                  | Port the management server listens on.                                                                                                            |
   | `management-server-secret`                | string    | _(random)_           | Secret for management server client authorization. Auto-generated if blank.                                                                       |
   | `management-server-tls-enabled`           | boolean   | `true`               | Whether the management server uses TLS.                                                                                                           |
   | `management-server-tls-keystore`          | string    | _(blank)_            | Path to the TLS keystore file. Required if TLS is enabled.                                                                                        |
   | `management-server-tls-keystore-password` | string    | _(blank)_            | Password for the TLS keystore. Can also be set via env var or JVM flag.                                                                           |
   | `max-chained-neighbor-updates`            | integer   | `1000000`            | Max consecutive neighbor updates before skipping. Negative = no limit.                                                                            |
   | `max-players`                             | integer   | `20`                 | Maximum players on the server at once.                                                                                                            |
   | `max-tick-time`                           | integer   | `60000`              | Max milliseconds per tick before the watchdog shuts down the server. `-1` disables.                                                               |
   | `max-world-size`                          | integer   | `29999984`           | Max world border radius in blocks. Must be between `1` and `29999984`.                                                                            |
   | `motd`                                    | string    | `A Minecraft Server` | Message shown in the server list. Supports color/formatting codes.                                                                                |
   | `network-compression-threshold`           | integer   | `256`                | Minimum packet size in bytes to compress. `-1` disables, `0` compresses all.                                                                      |
   | `online-mode`                             | boolean   | `true`               | Verifies players against Mojang account database. Disable only for offline/LAN servers.                                                           |
   | `op-permission-level`                     | integer   | `4`                  | Default permission level assigned when using `/op`. Must be between `0` and `4`.                                                                  |
   | `pause-when-empty-seconds`                | integer   | `60`                 | Seconds after all players leave before the server pauses.                                                                                         |
   | `player-idle-timeout`                     | integer   | `0`                  | Minutes before idle players are kicked. `0` = never.                                                                                              |
   | `prevent-proxy-connections`               | boolean   | `false`              | Kicks players whose ISP differs from Mojang's auth server.                                                                                        |
   | `query.port`                              | integer   | `25565`              | UDP port for the query server (requires `enable-query`).                                                                                          |
   | `rate-limit`                              | integer   | `0`                  | Max packets per second per player before kick. `0` disables.                                                                                      |
   | `rcon.password`                           | string    | _(blank)_            | RCON password. RCON won't start if blank and enabled.                                                                                             |
   | `rcon.port`                               | integer   | `25575`              | TCP port for RCON.                                                                                                                                |
   | `region-file-compression`                 | string    | `deflate`            | Chunk compression algorithm: `deflate`, `lz4`, or `none`.                                                                                         |
   | `require-resource-pack`                   | boolean   | `false`              | Disconnects players who decline the resource pack.                                                                                                |
   | `resource-pack`                           | string    | _(blank)_            | URL to an optional resource pack. Max 250 MiB.                                                                                                    |
   | `resource-pack-id`                        | UUID      | _(blank)_            | Optional UUID to identify the resource pack with clients.                                                                                         |
   | `resource-pack-prompt`                    | string    | _(blank)_            | Custom message shown on the resource pack prompt.                                                                                                 |
   | `resource-pack-sha1`                      | string    | _(blank)_            | SHA-1 hash of the resource pack for integrity verification.                                                                                       |
   | `server-ip`                               | string    | _(blank)_            | IP the server binds to. Leave blank to listen on all interfaces.                                                                                  |
   | `server-port`                             | integer   | `25565`              | TCP port the server listens on. Must be forwarded if behind NAT.                                                                                  |
   | `simulation-distance`                     | integer   | `10`                 | Chunk radius in which entities are ticked by the server. Must be between `3` and `32`.                                                            |
   | `spawn-protection`                        | integer   | `16`                 | Spawn protection radius as `2x+1` blocks. `0` disables.                                                                                           |
   | `status-heartbeat-interval`               | integer   | `0`                  | Interval in seconds for management server heartbeat notifications. `0` disables.                                                                  |
   | `sync-chunk-writes`                       | boolean   | `true`               | Enables synchronous chunk writes to prevent data loss on crash. May slow down I/O.                                                                |
   | `text-filtering-config`                   | string    | _(blank)_            | Chat filtering config. Used internally by Realms.                                                                                                 |
   | `text-filtering-version`                  | integer   | `0`                  | Config format version for `text-filtering-config`. Valid values: `0`, `1`.                                                                        |
   | `use-native-transport`                    | boolean   | `true`               | Enables Linux-optimized packet handling (Linux only).                                                                                             |
   | `view-distance`                           | integer   | `10`                 | Server-side view distance in chunks (radius). Must be between `3` and `32`.                                                                       |
   | `white-list`                              | boolean   | `false`              | Enables whitelist. Players not on it cannot connect. Ops are automatically whitelisted.                                                           |
   :::

   :::warning
   Do not change the `server-port` and `server-ip` settings.
   :::

    3. Click the save button in the bottom left corner.

   ---

4. Open the overview tab at the top.

5. Click the restart button in the control block.

## Adding plugins

:::warning
Plugins can only be added for the `Paper` loader.
:::

1. Open the servers page.

2. Find the server you want to add plugins in the table and click the first button in the actions column.

3. Upload plugins using one of the following methods:

:::details File manager
1. Open the files tab at the top.

2. Open the `plugins` folder in the file manager.

3. Click the upload button in the bottom left corner.

4. Select the plugins files from your device.

5. Click the upload button in the bottom right corner.
:::

8. Open the overview tab at the top.

9. Click the restart button in the control block.

## Adding mods

:::warning
Mods can only be added for the `Fabric` and `Forge` loaders.
:::

1. Open the servers page.

2. Find the server you want to add mods in the table and click the first button in the actions column.

3. Upload mods using one of the following methods:

:::details File manager
1. Open the files tab at the top.

2. Open the `mods` folder in the file manager.

3. Click the upload button in the bottom left corner.

4. Select the mods files from your device.

5. Click the upload button in the bottom right corner.
:::

4. Open the overview tab at the top.

5. Click the restart button in the control block.