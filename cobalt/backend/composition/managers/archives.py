#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.managers.archives import AbstractArchivesManager
from infrastructure.managers import ArchivesManager


def create_archives_manager() -> AbstractArchivesManager:
    """
    Creates the archives manager.

    Parameters:
    - None.

    Returns:
    - AbstractArchivesManager: AbstractArchivesManager object.
    """
    return ArchivesManager()
