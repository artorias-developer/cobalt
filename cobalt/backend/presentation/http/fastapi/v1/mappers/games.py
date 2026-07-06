#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from application.dtos import (
    GameDto,
    GamesGetPageDto,
    GamesPageDto
)
from presentation.contracts.http.mappers import (
    AbstractGamesRouterMapper,
    AbstractLoadersRouterMapper
)
from presentation.http.fastapi.v1.schemas import (
    GameSchema,
    GameShortSchema,
    GamesGetPageSchema,
    GamesPageSchema
)


class GamesRouterMapper(AbstractGamesRouterMapper):
    """
    Mapper for games router.
    """
    loaders_mapper: AbstractLoadersRouterMapper

    def __init__(
        self,
        loaders_mapper: AbstractLoadersRouterMapper
    ):
        self.loaders_mapper = loaders_mapper

    def dto_to_schema(
        self,
        dto: GameDto
    ) -> GameSchema:
        """
        Converts GameDto object to GameSchema object.

        Parameters:
        - dto: GameDto object.

        Returns:
        - GameSchema: GameSchema object.
        """
        return GameSchema(
            id=dto.id,
            name=dto.name,
            loaders=self.loaders_mapper.dtos_to_schemas(
                dtos=dto.loaders
            ),
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    def dtos_to_schemas(
        self,
        dtos: List[GameDto]
    ) -> List[GameSchema]:
        """
        Converts GameDto objects to GameSchema objects.

        Parameters:
        - dtos: List of GameDto objects.

        Returns:
        - List: List of GameSchema objects.
        """
        return [
            self.dto_to_schema(dto)
            for dto in dtos
        ]

    def dto_to_short_schema(
        self,
        dto: GameDto
    ) -> GameShortSchema:
        """
        Converts GameDto object to GameShortSchema object.

        Parameters:
        - dto: GameDto object.

        Returns:
        - GameShortSchema: GameShortSchema object.
        """
        return GameShortSchema(
            id=dto.id,
            name=dto.name,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    def page_dto_to_schema(
        self,
        dto: GamesPageDto
    ) -> GamesPageSchema:
        """
        Converts GamesPageDto object to GamesPageSchema object.

        Parameters:
        - dto: GamesPageDto object.

        Returns:
        - GamesPageSchema: GamesPageSchema object.
        """
        return GamesPageSchema(
            games=self.dtos_to_schemas(
                dtos=dto.games
            ),
            total=dto.total,
            page=dto.page,
            pages=dto.pages
        )

    def get_page_schema_to_dto(
        self,
        schema: GamesGetPageSchema
    ) -> GamesGetPageDto:
        """
        Converts GamesGetPageSchema object to GamesGetPageDto object.

        Parameters:
        - schema: GamesGetPageSchema object.

        Returns:
        - GamesGetPageDto: GamesGetPageDto object.
        """
        return GamesGetPageDto(
            page=schema.page,
            search=schema.search,
            sort_field=schema.sort_field,
            sort_direction=schema.sort_direction,
            limit=schema.limit
        )
