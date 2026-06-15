#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .dont_starve_together import DontStarveTogetherGameModule
from .factorio import FactorioGameModule
from .minecraft import MinecraftGameModule
from .rim_world import RimWorldGameModule
from .terraria import TerrariaGameModule

ENABLED_GAME_MODULES = [
    DontStarveTogetherGameModule,
    FactorioGameModule,
    MinecraftGameModule,
    RimWorldGameModule,
    TerrariaGameModule
]

__all__ = [
    "DontStarveTogetherGameModule",
    "FactorioGameModule",
    "MinecraftGameModule",
    "RimWorldGameModule",
    "TerrariaGameModule",
    "ENABLED_GAME_MODULES"
]
