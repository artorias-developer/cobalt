#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any

from application.dtos import (
    SettingsDto,
    SettingsUpdateDto
)


class AbstractSettingsRouterMapper(ABC):
    """
    Abstract mapper for settings router.
    """

    @abstractmethod
    def dto_to_schema(
        self,
        dto: SettingsDto
    ) -> Any:
        """
        Converts SettingsDto object to schema object.

        Parameters:
        - dto: SettingsDto object.

        Returns:
        - Any: Schema object.
        """
        ...

    @abstractmethod
    def update_schema_to_dto(
        self,
        schema: Any
    ) -> SettingsUpdateDto:
        """
        Converts schema object to SettingsUpdateDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - SettingsUpdateDto: SettingsUpdateDto object.
        """
        ...