#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from application.dtos import LoaderDto
from presentation.contracts.http.mappers import AbstractLoadersRouterMapper
from presentation.http.fastapi.v1.schemas import (
    LoaderSchema,
    LoaderShortSchema
)


class LoadersRouterMapper(AbstractLoadersRouterMapper):
    """
    Mapper for loaders router.
    """

    def dto_to_schema(
        self,
        dto: LoaderDto
    ) -> LoaderSchema:
        """
        Converts LoaderDto object to LoaderSchema object.

        Parameters:
        - dto: LoaderDto object.

        Returns:
        - LoaderSchema: LoaderSchema object.
        """
        return LoaderSchema(
            id=dto.id,
            game_id=dto.game_id,
            name=dto.name,
            versions=dto.versions,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    def dtos_to_schemas(
        self,
        dtos: List[LoaderDto]
    ) -> List[LoaderSchema]:
        """
        Converts LoaderDto objects to LoaderSchema objects.

        Parameters:
        - dtos: List of LoaderDto objects.

        Returns:
        - List: List of LoaderSchema objects.
        """
        return [
            self.dto_to_schema(dto)
            for dto in dtos
        ]

    def dto_to_short_schema(
        self,
        dto: LoaderDto
    ) -> LoaderShortSchema:
        """
        Converts LoaderDto object to LoaderShortSchema object.

        Parameters:
        - dto: LoaderDto object.

        Returns:
        - LoaderShortSchema: LoaderShortSchema object.
        """
        return LoaderShortSchema(
            id=dto.id,
            game_id=dto.game_id,
            name=dto.name,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )
