#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Any

from application.dtos import (
    AuthLoginDto,
    AuthChangeCredentialsDto
)


class AbstractAuthRouterMapper(ABC):
    """
    Abstract mapper for authentication router.
    """

    @abstractmethod
    def login_schema_to_dto(
        self,
        schema: Any
    ) -> AuthLoginDto:
        """
        Converts schema object to AuthLoginDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - AuthLoginDto: AuthLoginDto object.
        """
        ...

    @abstractmethod
    def change_credentials_schema_to_dto(
        self,
        schema: Any
    ) -> AuthChangeCredentialsDto:
        """
        Converts schema object to AuthChangeCredentialsDto object.

        Parameters:
        - schema: Schema object.

        Returns:
        - AuthChangeCredentialsDto: AuthChangeCredentialsDto object.
        """
        ...