#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.dtos import (
    AuthLoginDto,
    AuthUpdateCredentialsDto
)
from presentation.contracts.http.mappers import AbstractAuthRouterMapper
from presentation.http.fastapi.v1.schemas import (
    AuthLoginSchema,
    AuthChangeCredentialsSchema
)


class AuthRouterMapper(AbstractAuthRouterMapper):
    """
    Mapper for authentication router.
    """

    def login_schema_to_dto(
        self,
        schema: AuthLoginSchema
    ) -> AuthLoginDto:
        """
        Converts AuthLoginSchema object to AuthLoginDto object.

        Parameters:
        - schema: AuthLoginSchema object.

        Returns:
        - AuthLoginDto: AuthLoginDto object.
        """
        return AuthLoginDto(
            login=schema.login,
            password=schema.password
        )

    def change_credentials_schema_to_dto(
        self,
        schema: AuthChangeCredentialsSchema
    ) -> AuthUpdateCredentialsDto:
        """
        Converts AuthChangeCredentialsSchema to AuthUpdateCredentialsDto.

        Parameters:
        - schema: AuthChangeCredentialsSchema object.

        Returns:
        - AuthUpdateCredentialsDto: AuthUpdateCredentialsDto object.
        """
        return AuthUpdateCredentialsDto(
            login=schema.login,
            old_password=schema.old_password,
            new_password=schema.new_password
        )