#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod

from application.dtos import (
    SettingsDto,
    SettingsUpdateDto
)


class AbstractSettingsService(ABC):
    """
    Abstract settings service.
    """

    @abstractmethod
    async def update_one(
        self,
        user_id: int,
        dto: SettingsUpdateDto
    ) -> SettingsDto:
        """
        Updates existing settings.

        Parameters:
        - user_id: User ID.
        - dto: SettingsUpdateDto object.

        Returns:
        - SettingsDto: SettingsDto object.
        """
        ...

    @abstractmethod
    async def clear_cache(self) -> None:
        """
        Clears application cached data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def clear_containers(self) -> None:
        """
        Clears unused containers data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        ...