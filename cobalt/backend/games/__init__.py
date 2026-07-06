#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from .dont_starve_together import DontStarveTogetherGameModule
from .factorio import FactorioGameModule
from .minecraft import MinecraftGameModule
from .project_zomboid import ProjectZomboidGameModule
from .rim_world import RimWorldGameModule
from .seven_days_to_die import SevenDaysToDieGameModule
from .terraria import TerrariaGameModule

ENABLED_GAME_MODULES = [
    DontStarveTogetherGameModule,
    FactorioGameModule,
    MinecraftGameModule,
    ProjectZomboidGameModule,
    RimWorldGameModule,
    SevenDaysToDieGameModule,
    TerrariaGameModule
]

__all__ = [
    "DontStarveTogetherGameModule",
    "FactorioGameModule",
    "MinecraftGameModule",
    "ProjectZomboidGameModule",
    "RimWorldGameModule",
    "SevenDaysToDieGameModule",
    "TerrariaGameModule",
    "ENABLED_GAME_MODULES"
]
