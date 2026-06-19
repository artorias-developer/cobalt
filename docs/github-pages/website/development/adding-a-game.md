# Adding a game

This guide explains how to add support for a new game to Cobalt.

## Backend

1. Create a new game directory in `cobalt/backend/games/`, e.g. `new_game`. This will hold everything related to the game, including all of its loaders (vanilla, modded, etc).

2. In the root of `new_game`, create a package named after the loader, e.g. `vanilla`. All files related to that specific loader live here.

:::tip
A package is a directory with an `__init__.py` file inside.
:::

:::tip
A single game can have multiple loaders, each in its own package.
:::

3. Inside the loader package, create `infrastructure/loader.py`. This class is responsible for fetching and parsing the list of available game versions for this loader, and building the download link for a specific version.

:::info Example
[Terraria's vanilla loader](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/vanilla/infrastructure/loader.py)
:::

4. Inside the loader package, create `infrastructure/__init__.py`.

:::info Example
[Terraria's vanilla infrastructure package](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/vanilla/infrastructure/__init__.py)
:::

5. Inside the loader package, create `application/services/servers.py`. This service is responsible for creating a server by building and starting the Docker containers defined in steps 6 and 7, and passing them the required data (version, download link, etc).

:::info Example
[Terraria's vanilla service](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/vanilla/application/services/servers.py)
:::

6. Inside the loader package, create `application/services/__init__.py`.

:::info Example
[Terraria's vanilla services package](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/vanilla/application/services/__init__.py)
:::

7. Inside the loader package, create `build/Container.installer`. This container simply downloads all the server files into the server's isolated directory.

:::info Example
[Terraria's vanilla installer](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/vanilla/build/Container.installer)
:::

8. Inside the loader package, create `build/Container.runtime`. This container runs the actual game server from the isolated directory created in step 7.

:::info Example
[Terraria's vanilla runtime](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/vanilla/build/Container.runtime)
:::

9. Inside the loader package, create `build/scripts/entrypoint.sh`. This is the entrypoint for the runtime container from step 8 - it's responsible for starting the server, creating a FIFO file to pass commands from the dashboard, and gracefully shutting down the server on a stop command.

:::info Example
[Terraria's vanilla entrypoint](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/vanilla/build/scripts/entrypoint.sh)
:::

10. In the root of `new_game`, create `module.py`. This module initializes all of the game's loaders. Under the hood, it also automatically checks whether the game and its loaders already exist in the database, and adds them if they don't.

:::info Example
[Terraria module](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/module.py)
:::

11. In the root of `new_game`, create `__init__.py` that exports the game module.

:::info Example
[Terraria package](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/__init__.py)
:::

12. Register the new game module in `cobalt/backend/games/__init__.py` by adding it to `ENABLED_GAME_MODULES`:

```python
from .dont_starve_together import DontStarveTogetherGameModule
...
from .new_game import NewGameModule # [!code ++]

ENABLED_GAME_MODULES = [
    DontStarveTogetherGameModule,
    ...,
    NewGameModule # [!code ++]
]
```

## Frontend

1. Create a new game directory in `cobalt/frontend/src/assets/images/games/`, e.g. `new-game`. Add the following assets to it:

    * `icon.png`
        * max_width: 200x200

    * `background.png`
        * max_width: 1920x1080

    [Compress](https://www.iloveimg.com/compress-image) all images beforehand.

2. In `cobalt/frontend/src/utils/games.ts`, import the icon:

```typescript
import newGameIcon from "@/assets/images/games/new-game/icon.png"
```

3. In the same file, add an entry to `GameModules`:

```typescript
new_game: {
  displayName: "NewGame",
  icon: newGameIcon,
  loaders: {
    vanilla: {
      displayName: "Vanilla"
    }
  },
  sort_number: 6
}
```

This is used to display the game in the server creation form.

4. Create `cobalt/frontend/src/pages/games/new-game/ServerPage.vue`. This is the page that gets rendered when a user opens a server of this game.

:::info Example
[Terraria's ServerPage](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/frontend/src/pages/games/terraria/ServerPage.vue)
:::

5. In `cobalt/frontend/src/pages/ServerPage.vue`, register the new page in `gameComponents`:

```typescript
const gameComponents: Record<string, Component> = {
  dont_starve_together: DontStarveTogetherServerPage,
  ...,
  new_game: NewGameServerPage // [!code ++]
}
```

This map tells the app which page component to render based on the game type of the opened server.