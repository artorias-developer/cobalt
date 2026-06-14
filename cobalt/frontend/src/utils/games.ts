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

export const GameModules: GameModulesMap = {
  minecraft: {
    displayName: "Minecraft",
    description: "Mine resources, craft tools and survive in an infinite world.",
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
    description: "Explore caves, fight bosses, and build in 2D world.",
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
    description: "Survive the wilderness together in a dark world.",
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
    description: "Build and automate factories while surviving alien attacks.",
    icon: factorioIcon,
    loaders: {
      vanilla: {
        displayName: "Vanilla"
      }
    },
    sort_number: 4
  }
}