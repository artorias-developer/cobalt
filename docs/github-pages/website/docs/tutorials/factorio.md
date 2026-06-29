# Factorio

This tutorial explains how to set up a Factorio server in the Cobalt dashboard.

## Adding a token

Immediately after creating the server, you may see the message `Error when creating server game: Missing token` in the console. This token is required for the server to appear in the game's search results.

:::tip
This is an optional setting, you will still be able to connect to the server using IP.
:::

1. [Log in](https://factorio.com/login) to your Factorio account.

2. Go to the [profile](https://www.factorio.com/profile) page.

3. Copy the `username` and `token` values.

4. Go to the Cobalt dashboard.

5. Open the servers page.

6. Find the server you want to add token in the table and click the first button in the actions column.

7. Open the files tab at the top.

8. Open the `data/server-settings.json` file in the file editor.

9. Insert the values for `username` and `token` into the appropriate fields.

10. Click the save button in the bottom left corner.

11. Open the overview tab at the top.

12. Click the restart button in the control block.

## Changing configs

1. Open the servers page.

2. Find the server you want to change settings in the table and click the first button in the actions column.

3. Open the files tab at the top.

   ---

   ### `map-gen-settings.json`

   1. Open the `data/map-gen-settings.json` file in the file editor.

   2. Update the settings.

   :::details List of settings
   
   This table refers to version `2.0.77`. Some settings may not be available in earlier versions.

   <div class="table map-gen-settings">   

   | Key                                                    | Type     | Default              | Description                                                                                                                                                                     |
   |--------------------------------------------------------|----------|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
   | `width`                                                | integer  | `0`                  | Width of the map, in tiles. `0` means infinite.                                                                                                                                 |
   | `height`                                               | integer  | `0`                  | Height of the map, in tiles. `0` means infinite.                                                                                                                                |
   | `starting_area`                                        | number   | `1`                  | Multiplier for the "biter free zone radius".                                                                                                                                    |
   | `peaceful_mode`                                        | boolean  | `false`              | Enables peaceful mode.<br>`true` - enabled<br>`false` - disabled                                                                                                                |
   | `autoplace_controls.coal.frequency`                    | number   | `1`                  | Frequency of coal ore patches.                                                                                                                                                  |
   | `autoplace_controls.coal.size`                         | number   | `1`                  | Size of coal ore patches.                                                                                                                                                       |
   | `autoplace_controls.coal.richness`                     | number   | `1`                  | Richness of coal ore patches.                                                                                                                                                   |
   | `autoplace_controls.stone.frequency`                   | number   | `1`                  | Frequency of stone ore patches.                                                                                                                                                 |
   | `autoplace_controls.stone.size`                        | number   | `1`                  | Size of stone ore patches.                                                                                                                                                      |
   | `autoplace_controls.stone.richness`                    | number   | `1`                  | Richness of stone ore patches.                                                                                                                                                  |
   | `autoplace_controls.copper-ore.frequency`              | number   | `1`                  | Frequency of copper ore patches.                                                                                                                                                |
   | `autoplace_controls.copper-ore.size`                   | number   | `1`                  | Size of copper ore patches.                                                                                                                                                     |
   | `autoplace_controls.copper-ore.richness`               | number   | `1`                  | Richness of copper ore patches.                                                                                                                                                 |
   | `autoplace_controls.iron-ore.frequency`                | number   | `1`                  | Frequency of iron ore patches.                                                                                                                                                  |
   | `autoplace_controls.iron-ore.size`                     | number   | `1`                  | Size of iron ore patches.                                                                                                                                                       |
   | `autoplace_controls.iron-ore.richness`                 | number   | `1`                  | Richness of iron ore patches.                                                                                                                                                   |
   | `autoplace_controls.uranium-ore.frequency`             | number   | `1`                  | Frequency of uranium ore patches.                                                                                                                                               |
   | `autoplace_controls.uranium-ore.size`                  | number   | `1`                  | Size of uranium ore patches.                                                                                                                                                    |
   | `autoplace_controls.uranium-ore.richness`              | number   | `1`                  | Richness of uranium ore patches.                                                                                                                                                |
   | `autoplace_controls.crude-oil.frequency`               | number   | `1`                  | Frequency of crude oil patches.                                                                                                                                                 |
   | `autoplace_controls.crude-oil.size`                    | number   | `1`                  | Size of crude oil patches.                                                                                                                                                      |
   | `autoplace_controls.crude-oil.richness`                | number   | `1`                  | Richness of crude oil patches.                                                                                                                                                  |
   | `autoplace_controls.water.frequency`                   | number   | `1`                  | Frequency of water.                                                                                                                                                             |
   | `autoplace_controls.water.size`                        | number   | `1`                  | Size of water bodies.                                                                                                                                                           |
   | `autoplace_controls.trees.frequency`                   | number   | `1`                  | Frequency of trees.                                                                                                                                                             |
   | `autoplace_controls.trees.size`                        | number   | `1`                  | Size of tree clusters.                                                                                                                                                          |
   | `autoplace_controls.enemy-base.frequency`              | number   | `1`                  | Frequency of enemy bases.                                                                                                                                                       |
   | `autoplace_controls.enemy-base.size`                   | number   | `1`                  | Size of enemy bases.                                                                                                                                                            |
   | `cliff_settings.name`                                  | string   | `cliff`              | Name of the cliff prototype.                                                                                                                                                    |
   | `cliff_settings.cliff_elevation_0`                     | number   | `10`                 | Elevation of the first row of cliffs.                                                                                                                                           |
   | `cliff_settings.cliff_elevation_interval`              | number   | `40`                 | Elevation difference between successive rows of cliffs. Inversely proportional to "frequency" in the map generation GUI - when set from the GUI, the value is `40 / frequency`. |
   | `cliff_settings.richness`                              | number   | `1`                  | Called "cliff continuity" in the map generator GUI. `0` results in no cliffs, `10` makes all cliff rows completely solid.                                                       |
   | `property_expression_names.control:moisture:frequency` | string   | `1`                  | Inverse of the "moisture scale" in the map generator GUI.                                                                                                                       |
   | `property_expression_names.control:moisture:bias`      | string   | `0`                  | The "moisture bias" in the map generator GUI.                                                                                                                                   |
   | `property_expression_names.control:aux:frequency`      | string   | `1`                  | Inverse of the "terrain type scale" in the map generator GUI.                                                                                                                   |
   | `property_expression_names.control:aux:bias`           | string   | `0`                  | The "terrain type bias" in the map generator GUI.                                                                                                                               |
   | `starting_points`                                      | array    | `[{"x": 0, "y": 0}]` | List of starting point coordinates for players.                                                                                                                                 |
   | `seed`                                                 | integer  | `null`               | World seed. Use `null` for a random seed, or a number for a specific seed.                                                                                                      |
   </div>
   :::

   :::warning
   After changing the settings, delete the `saves/map.zip` file so that the map will be regenerated when the server restarts.
   :::

   3. Click the save button in the bottom left corner.

   ---

   ### `map-settings.json`

   1. Open the `data/map-settings.json` file in the file editor.

   2. Update the settings.

   :::details List of settings

   This table refers to version `2.0.77`. Some settings may not be available in earlier versions.
   
   <div class="table map-settings">

   | Key                                                                | Type    | Default         | Description  |
   |--------------------------------------------------------------------|---------|-----------------|--------------|
   | `difficulty_settings.technology_price_multiplier`                  | number  | `1`             |              |
   | `difficulty_settings.spoil_time_modifier`                          | number  | `1`             |              |
   | `pollution.enabled`                                                | boolean | `true`          |              |
   | `pollution.diffusion_ratio`                                        | number  | `0.02`          |              |
   | `pollution.min_to_diffuse`                                         | number  | `15`            |              |
   | `pollution.ageing`                                                 | number  | `1`             |              |
   | `pollution.expected_max_per_chunk`                                 | number  | `150`           |              |
   | `pollution.min_to_show_per_chunk`                                  | number  | `50`            |              |
   | `pollution.min_pollution_to_damage_trees`                          | number  | `60`            |              |
   | `pollution.pollution_with_max_forest_damage`                       | number  | `150`           |              |
   | `pollution.pollution_per_tree_damage`                              | number  | `50`            |              |
   | `pollution.pollution_restored_per_tree_damage`                     | number  | `10`            |              |
   | `pollution.max_pollution_to_restore_trees`                         | number  | `20`            |              |
   | `pollution.enemy_attack_pollution_consumption_modifier`            | number  | `1`             |              |
   | `enemy_evolution.enabled`                                          | boolean | `true`          |              |
   | `enemy_evolution.time_factor`                                      | number  | `0.000004`      |              |
   | `enemy_evolution.destroy_factor`                                   | number  | `0.002`         |              |
   | `enemy_evolution.pollution_factor`                                 | number  | `0.0000009`     |              |
   | `enemy_expansion.enabled`                                          | boolean | `true`          |              |
   | `enemy_expansion.max_expansion_distance`                           | number  | `7`             |              |
   | `enemy_expansion.friendly_base_influence_radius`                   | number  | `2`             |              |
   | `enemy_expansion.enemy_building_influence_radius`                  | number  | `2`             |              |
   | `enemy_expansion.building_coefficient`                             | number  | `0.1`           |              |
   | `enemy_expansion.other_base_coefficient`                           | number  | `2.0`           |              |
   | `enemy_expansion.neighbouring_chunk_coefficient`                   | number  | `0.5`           |              |
   | `enemy_expansion.neighbouring_base_chunk_coefficient`              | number  | `0.4`           |              |
   | `enemy_expansion.max_colliding_tiles_coefficient`                  | number  | `0.9`           |              |
   | `enemy_expansion.settler_group_min_size`                           | number  | `5`             |              |
   | `enemy_expansion.settler_group_max_size`                           | number  | `20`            |              |
   | `enemy_expansion.min_expansion_cooldown`                           | number  | `14400`         |              |
   | `enemy_expansion.max_expansion_cooldown`                           | number  | `216000`        |              |
   | `unit_group.min_group_gathering_time`                              | number  | `3600`          |              |
   | `unit_group.max_group_gathering_time`                              | number  | `36000`         |              |
   | `unit_group.max_wait_time_for_late_members`                        | number  | `7200`          |              |
   | `unit_group.max_group_radius`                                      | number  | `30.0`          |              |
   | `unit_group.min_group_radius`                                      | number  | `5.0`           |              |
   | `unit_group.max_member_speedup_when_behind`                        | number  | `1.4`           |              |
   | `unit_group.max_member_slowdown_when_ahead`                        | number  | `0.6`           |              |
   | `unit_group.max_group_slowdown_factor`                             | number  | `0.3`           |              |
   | `unit_group.max_group_member_fallback_factor`                      | number  | `3`             |              |
   | `unit_group.member_disown_distance`                                | number  | `10`            |              |
   | `unit_group.tick_tolerance_when_member_arrives`                    | number  | `60`            |              |
   | `unit_group.max_gathering_unit_groups`                             | number  | `30`            |              |
   | `unit_group.max_unit_group_size`                                   | number  | `200`           |              |
   | `steering.default.radius`                                          | number  | `1.2`           |              |
   | `steering.default.separation_force`                                | number  | `0.005`         |              |
   | `steering.default.separation_factor`                               | number  | `1.2`           |              |
   | `steering.default.force_unit_fuzzy_goto_behavior`                  | boolean | `false`         |              |
   | `steering.moving.radius`                                           | number  | `3`             |              |
   | `steering.moving.separation_force`                                 | number  | `0.01`          |              |
   | `steering.moving.separation_factor`                                | number  | `3`             |              |
   | `steering.moving.force_unit_fuzzy_goto_behavior`                   | boolean | `false`         |              |
   | `path_finder.fwd2bwd_ratio`                                        | number  | `5`             |              |
   | `path_finder.goal_pressure_ratio`                                  | number  | `2`             |              |
   | `path_finder.max_steps_worked_per_tick`                            | number  | `1000`          |              |
   | `path_finder.max_work_done_per_tick`                               | number  | `8000`          |              |
   | `path_finder.use_path_cache`                                       | boolean | `true`          |              |
   | `path_finder.short_cache_size`                                     | number  | `5`             |              |
   | `path_finder.long_cache_size`                                      | number  | `25`            |              |
   | `path_finder.short_cache_min_cacheable_distance`                   | number  | `10`            |              |
   | `path_finder.short_cache_min_algo_steps_to_cache`                  | number  | `50`            |              |
   | `path_finder.long_cache_min_cacheable_distance`                    | number  | `30`            |              |
   | `path_finder.cache_max_connect_to_cache_steps_multiplier`          | number  | `100`           |              |
   | `path_finder.cache_accept_path_start_distance_ratio`               | number  | `0.2`           |              |
   | `path_finder.cache_accept_path_end_distance_ratio`                 | number  | `0.15`          |              |
   | `path_finder.negative_cache_accept_path_start_distance_ratio`      | number  | `0.3`           |              |
   | `path_finder.negative_cache_accept_path_end_distance_ratio`        | number  | `0.3`           |              |
   | `path_finder.cache_path_start_distance_rating_multiplier`          | number  | `10`            |              |
   | `path_finder.cache_path_end_distance_rating_multiplier`            | number  | `20`            |              |
   | `path_finder.stale_enemy_with_same_destination_collision_penalty`  | number  | `30`            |              |
   | `path_finder.ignore_moving_enemy_collision_distance`               | number  | `5`             |              |
   | `path_finder.enemy_with_different_destination_collision_penalty`   | number  | `30`            |              |
   | `path_finder.general_entity_collision_penalty`                     | number  | `10`            |              |
   | `path_finder.general_entity_subsequent_collision_penalty`          | number  | `3`             |              |
   | `path_finder.extended_collision_penalty`                           | number  | `3`             |              |
   | `path_finder.max_clients_to_accept_any_new_request`                | number  | `10`            |              |
   | `path_finder.max_clients_to_accept_short_new_request`              | number  | `100`           |              |
   | `path_finder.direct_distance_to_consider_short_request`            | number  | `100`           |              |
   | `path_finder.short_request_max_steps`                              | number  | `1000`          |              |
   | `path_finder.short_request_ratio`                                  | number  | `0.5`           |              |
   | `path_finder.min_steps_to_check_path_find_termination`             | number  | `2000`          |              |
   | `path_finder.start_to_goal_cost_multiplier_to_terminate_path_find` | number  | `2000.0`        |              |
   | `path_finder.overload_levels`                                      | array   | `[0, 100, 500]` |              |
   | `path_finder.overload_multipliers`                                 | array   | `[2, 3, 4]`     |              |
   | `path_finder.negative_path_cache_delay_interval`                   | number  | `20`            |              |
   | `asteroids.spawning_rate`                                          | number  | `1`             |              |
   | `asteroids.max_ray_portals_expanded_per_tick`                      | number  | `100`           |              |
   | `max_failed_behavior_count`                                        | number  | `3`             |              |
   </div>
   :::

   3. Click the save button in the bottom left corner.

   ---

   ### `server-settings.json`

   1. Open the `data/server-settings.json` file in the file editor.

   2. Update the settings.

   :::details List of settings

   This table refers to version `2.0.77`. Some settings may not be available in earlier versions. Cobalt overrides some default values when a server is created.
   
   <div class="table server-settings">
   
   | Key                                              | Type    | Default            | Description                                                                                                                                                                                                                                                                                                                                                                                                         |
   |--------------------------------------------------|---------|--------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
   | `name`                                           | string  | _(blank)_          | Name of the game as it will appear in the game listing.                                                                                                                                                                                                                                                                                                                                                             |
   | `description`                                    | string  | _(blank)_          | Description of the game that will appear in the listing.                                                                                                                                                                                                                                                                                                                                                            |
   | `tags`                                           | array   | `["game", "tags"]` | Tags for the game listing.                                                                                                                                                                                                                                                                                                                                                                                          |
   | `max_players`                                    | integer | `0`                | Maximum number of players allowed, admins can join even a full server. `0` means unlimited.                                                                                                                                                                                                                                                                                                                         |
   | `visibility.public`                              | boolean | `true`             | Game will be published on the official Factorio matching server.                                                                                                                                                                                                                                                                                                                                                    |
   | `visibility.lan`                                 | boolean | `true`             | Game will be broadcast on LAN.                                                                                                                                                                                                                                                                                                                                                                                      |
   | `username`                                       | string  | _(blank)_          | Your factorio.com login credentials. Required for games with visibility `public`.                                                                                                                                                                                                                                                                                                                                   |
   | `password`                                       | string  | _(blank)_          | Your factorio.com login credentials. Required for games with visibility `public`.                                                                                                                                                                                                                                                                                                                                   |
   | `token`                                          | string  | _(blank)_          | Authentication token. May be used instead of `password` above.                                                                                                                                                                                                                                                                                                                                                      |
   | `game_password`                                  | string  | _(blank)_          | The password required for players to join the game.                                                                                                                                                                                                                                                                                                                                                                 |
   | `require_user_verification`                      | boolean | `true`             | When set to `true`, the server will only allow clients that have a valid Factorio.com account.                                                                                                                                                                                                                                                                                                                      |
   | `max_upload_in_kilobytes_per_second`             | integer | `0`                | Optional, default value is `0`. `0` means unlimited.                                                                                                                                                                                                                                                                                                                                                                |
   | `max_upload_slots`                               | integer | `5`                | Optional, default value is `5`. `0` means unlimited.                                                                                                                                                                                                                                                                                                                                                                |
   | `minimum_latency_in_ticks`                       | integer | `0`                | Optional, one tick is 16ms at default speed. Default value is `0`. `0` means no minimum.                                                                                                                                                                                                                                                                                                                            |
   | `max_heartbeats_per_second`                      | integer | `60`               | Network tick rate. Maximum rate game update packets are sent at before bundling them together. Minimum value is `6`, maximum value is `240`.                                                                                                                                                                                                                                                                        |
   | `ignore_player_limit_for_returning_players`      | boolean | `false`            | Players that already played on this map can join even when the max player limit was reached.                                                                                                                                                                                                                                                                                                                        |
   | `allow_commands`                                 | string  | `admins-only`      | Possible values are `true`, `false`, and `admins-only`.                                                                                                                                                                                                                                                                                                                                                             |
   | `autosave_interval`                              | integer | `10`               | Autosave interval, in minutes.                                                                                                                                                                                                                                                                                                                                                                                      |
   | `autosave_slots`                                 | integer | `5`                | Server autosave slots. Cycled through when the server autosaves.                                                                                                                                                                                                                                                                                                                                                    |
   | `afk_autokick_interval`                          | integer | `0`                | How many minutes until someone is kicked for doing nothing. `0` for never.                                                                                                                                                                                                                                                                                                                                          |
   | `auto_pause`                                     | boolean | `true`             | Whether the server should be paused when no players are present.                                                                                                                                                                                                                                                                                                                                                    |
   | `auto_pause_when_players_connect`                | boolean | `false`            | Whether the server should be paused when someone is connecting to the server.                                                                                                                                                                                                                                                                                                                                       |
   | `only_admins_can_pause_the_game`                 | boolean | `true`             | Whether only admins are allowed to pause the game.                                                                                                                                                                                                                                                                                                                                                                  |
   | `autosave_only_on_server`                        | boolean | `true`             | Whether autosaves should be saved only on the server or also on all connected clients. Default is `true`.                                                                                                                                                                                                                                                                                                           |
   | `non_blocking_saving`                            | boolean | `false`            | Highly experimental feature, enable only at your own risk of losing your saves. On UNIX systems, the server will fork itself to create an autosave. Autosaving on connected Windows clients will be disabled regardless of the `autosave_only_on_server` option.                                                                                                                                                    |
   | `minimum_segment_size`                           | integer | `25`               | Long network messages are split into segments sent over multiple ticks. Their size depends on the number of peers currently connected. Increasing the segment size increases upload bandwidth requirements for the server and download bandwidth requirements for clients. This setting only affects server outbound messages. Changing these settings can negatively impact connection stability for some clients. |
   | `minimum_segment_size_peer_count`                | integer | `20`               | See `minimum_segment_size` above.                                                                                                                                                                                                                                                                                                                                                                                   |
   | `maximum_segment_size`                           | integer | `100`              | See `minimum_segment_size` above.                                                                                                                                                                                                                                                                                                                                                                                   |
   | `maximum_segment_size_peer_count`                | integer | `10`               | See `minimum_segment_size` above.                                                                                                                                                                                                                                                                                                                                                                                   |
   </div>
   :::

   3. Click the save button in the bottom left corner.

   ---

4. Open the overview tab at the top.

5. Click the restart button in the control block.

## Adding mods

1. Open the servers page.

2. Find the server you want to add mods in the table and click the first button in the actions column.

3. Upload mods using one of the following methods:

::::details File manager
1. Open the files tab at the top.

2. Open the `mods` folder in the file manager.

3. Click the upload button in the bottom left corner.

4. Select the mods files from your device.

:::tip
You can find mods on the [Factorio Mods website](https://mods.factorio.com).
:::

5. Click the upload button in the bottom right corner.
::::

[//]: # (::::details Configuration file)

[//]: # ()
[//]: # (:::warning )

[//]: # (For this method, you need to [add a token]&#40;#adding-a-token&#41;.)

[//]: # (:::)

[//]: # ()
[//]: # (1. Click the stop button in the control block.)

[//]: # ()
[//]: # (2. Open the files tab at the top.)

[//]: # ()
[//]: # (3. Open the `mods/mod-list.json` file in the file editor.)

[//]: # ()
[//]: # (4. Add the mod to the list using its name:)

[//]: # ()
[//]: # (```json)

[//]: # ({)

[//]: # (   "mods": [)

[//]: # (      ...,)

[//]: # (      {)

[//]: # (         "name": "space-age",)

[//]: # (         "enabled": true)

[//]: # (      },)

[//]: # (      { // [!code ++])

[//]: # (         "name": "molten_plastic", // [!code ++])

[//]: # (         "enabled": true // [!code ++])

[//]: # (      } // [!code ++])

[//]: # (   ])

[//]: # (})

[//]: # (```)

[//]: # ()
[//]: # (:::tip)

[//]: # (You can get the name from the link on the [Factorio Mods website]&#40;https://mods.factorio.com&#41;.)

[//]: # ()
[//]: # (Example: https://mods.factorio.com/mod/molten_plastic?from=updated)

[//]: # ()
[//]: # (In this case, the name is `molten_plastic`.)

[//]: # (:::)

[//]: # ()
[//]: # (5. Click the save button in the bottom left corner.)

[//]: # (::::)

4. Open the overview tab at the top.

5. Click the restart button in the control block.


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
   min-width: 200px; 
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

.table.map-settings th:nth-child(4),
.table.map-settings td:nth-child(4) {
   display: none;
}
</style>