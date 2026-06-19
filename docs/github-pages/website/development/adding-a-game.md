# Adding a game

This guide explains how to add support for a new game to Cobalt.

## Backend

1. Create a new game directory in `cobalt/backend/games/`, e.g. `new_game`. This will hold everything related to the game, including all of its loaders (vanilla, modded, etc).

2. In the root of `new_game`, create a package (a directory with `__init__.py`) named after the loader, e.g. `vanilla`. All files related to that specific loader live here. A single game can have multiple loaders, each in its own package.

3. Inside the loader package, create `infrastructure/loader.py`, following the [example for Terraria's vanilla loader](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/vanilla/infrastructure/loader.py). This class is responsible for fetching and parsing the list of available game versions for this loader, and building the download link for a specific version.

4. Inside the loader package, create `application/services/servers.py`, following the [example for Terraria's vanilla service](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/vanilla/application/services/servers.py). This service is responsible for creating a server by building and starting the Docker containers defined in steps 5 and 6, and passing them the required data (version, download link, etc).

5. Inside the loader package, create `build/Container.installer`, following the [example for Terraria's vanilla installer](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/vanilla/build/Container.installer). This container simply downloads all the server files into the server's isolated directory.

6. Inside the loader package, create `build/Container.runtime`, following the [example for Terraria's vanilla runtime](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/vanilla/build/Container.runtime). This container runs the actual game server from the isolated directory created in step 5.

7. Inside the loader package, create `build/scripts/entrypoint.sh`, following the [example for Terraria's vanilla entrypoint](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/vanilla/build/scripts/entrypoint.sh). This is the entrypoint for the runtime container from step 6 - it's responsible for starting the server, creating a FIFO file to pass commands from the dashboard, and gracefully shutting down the server on a stop command.

8. In the root of `new_game`, create `module.py`, following the [example for the Terraria module](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/module.py). This module initializes all of the game's loaders. Under the hood, it also automatically checks whether the game and its loaders already exist in the database, and adds them if they don't.

9. In the root of `new_game`, create `__init__.py` that exports the game module, following the [example for the Terraria package](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/backend/games/terraria/__init__.py).


10. Register the new game module in `cobalt/backend/games/__init__.py` by adding it to `ENABLED_GAME_MODULES`:

```python
from .new_game import NewGameModule

ENABLED_GAME_MODULES = [
    ...,
    NewGameModule
]
```

## Frontend

1. Create a new game directory in `cobalt/frontend/src/assets/images/games/`, e.g. `new-game`. Add an icon (max 200px on the largest side) and a background (no larger than 1920x1080) to it. [Compress](https://www.iloveimg.com/compress-image) them beforehand.

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

This is used to display the game in the server creation form - with its name, icon, and available loaders:

4. Create `cobalt/frontend/src/pages/games/new-game/ServerPage.vue`, following the [example for Terraria's ServerPage](https://github.com/ArtoriasCode/cobalt/blob/main/cobalt/frontend/src/pages/games/terraria/ServerPage.vue). This is the page that gets rendered when a user opens a server of this game.

5. In `cobalt/frontend/src/pages/ServerPage.vue`, register the new page in `gameComponents`:

```typescript
const gameComponents: Record<string, Component> = {
  ...,
  new_game: NewGameServerPage
}
```

This map tells the app which page component to render based on the game type of the opened server.