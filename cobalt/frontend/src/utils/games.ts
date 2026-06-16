/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { GameModulesMap } from "@/types"

import dontStarveTogetherIcon from "@/assets/images/games/dont-starve-together/icon.png"
import factorioIcon from "@/assets/images/games/factorio/icon.png"
import minecraftIcon from "@/assets/images/games/minecraft/icon.png"
import terrariaIcon from "@/assets/images/games/terraria/icon.png"
import rimWorldIcon from "@/assets/images/games/rim-world/icon.png"

export const GameModules: GameModulesMap = {
  minecraft: {
    displayName: "Minecraft",
    icon: minecraftIcon,
    loaders: {
      fabric: {
        displayName: "Fabric"
      },
      forge: {
        displayName: "Forge"
      },
      paper: {
        displayName: "Paper"
      }
    },
    sort_number: 1
  },
  terraria: {
    displayName: "Terraria",
    icon: terrariaIcon,
    loaders: {
      vanilla: {
        displayName: "Vanilla"
      },
      tmodloader: {
        displayName: "tModLoader"
      }
    },
    sort_number: 2
  },
  dont_starve_together: {
    displayName: "Don't Starve Together",
    icon: dontStarveTogetherIcon,
    loaders: {
      vanilla: {
        displayName: "Vanilla"
      }
    },
    sort_number: 3
  },
  factorio: {
    displayName: "Factorio",
    icon: factorioIcon,
    loaders: {
      vanilla: {
        displayName: "Vanilla"
      }
    },
    sort_number: 4
  },
  rim_world: {
    displayName: "RimWorld",
    icon: rimWorldIcon,
    loaders: {
      together: {
        displayName: "Together"
      }
    },
    sort_number: 5
  }
}