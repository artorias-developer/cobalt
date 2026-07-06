#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Optional, Any

from domain.entities import SettingsEntity, SettingsUpdateEntity


class AbstractSettingsRepository(ABC):
    """
    Abstract settings repository.
    """

    @abstractmethod
    async def update_one(
        self,
        user_id: int,
        entity: SettingsUpdateEntity,
        session: Optional[Any] = None
    ) -> Optional[SettingsEntity]:
        """
        Updates existing settings.

        Parameters:
        - user_id: User ID.
        - entity: SettingsUpdateEntity object.
        - session: Session object.

        Returns:
        - SettingsEntity: SettingsEntity object.
        """
        ...