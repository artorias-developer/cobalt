#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

def get_java_version(
    version: str
) -> str:
    """
    Returns the required Java version for a given Minecraft version.

    Parameters:
    - version: Minecraft version.

    Returns:
    - str: Required Java version.
    """
    parts = version.split(".")
    major = int(parts[0]) if len(parts) > 1 else 0
    minor = int(parts[1]) if len(parts) > 1 else 0

    if major == 1 and minor <= 16:
        return "8"

    if major == 1 and minor <= 19:
        return "17"

    if major == 1 and minor <= 21:
        return "21"

    return "25"