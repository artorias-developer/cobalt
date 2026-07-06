#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from domain.value_objects import GameName
from domain.entities import (
    GameEntity,
    GamesPageEntity,
    GamesGetPageEntity,
    GameCreateEntity,
    GameUpdateEntity
)
from application.contracts.mappers import (
    AbstractGamesServiceMapper,
    AbstractLoadersServiceMapper
)
from application.dtos import (
    GameDto,
    GamesPageDto,
    GamesGetPageDto,
    GameCreateDto,
    GameUpdateDto
)


class GamesServiceMapper(AbstractGamesServiceMapper):
    """
    Mapper for games service.
    """
    loaders_mapper: AbstractLoadersServiceMapper

    def __init__(
        self,
        loaders_mapper: AbstractLoadersServiceMapper
    ):
        self.loaders_mapper = loaders_mapper
        
    def entity_to_dto(
        self,
        entity: GameEntity
    ) -> GameDto:
        """
        Converts GameEntity object to GameDto object.

        Parameters:
        - entity: GameEntity object.

        Returns:
        - GameDto: GameDto object.
        """
        return GameDto(
            id=entity.id,
            name=entity.name.value,
            loaders=self.loaders_mapper.entities_to_dtos(
                entities=entity.loaders
            ),
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def entities_to_dtos(
        self,
        entities: List[GameEntity]
    ) -> List[GameDto]:
        """
        Converts GameEntity objects to GameDto objects.

        Parameters:
        - entities: List of GameEntity objects.

        Returns:
        - List: List of GameDto objects.
        """
        return [
            self.entity_to_dto(entity)
            for entity in entities
        ]

    def page_entity_to_dto(
        self,
        entity: GamesPageEntity
    ) -> GamesPageDto:
        """
        Converts GamesPageEntity object to GamesPageDto object.

        Parameters:
        - entity: GamesPageEntity object.

        Returns:
        - GamesPageDto: GamesPageDto object.
        """
        return GamesPageDto(
            games=self.entities_to_dtos(
                entities=entity.games
            ),
            total=entity.total,
            page=entity.page,
            pages=entity.pages
        )

    def get_page_dto_to_entity(
        self,
        dto: GamesGetPageDto
    ) -> GamesGetPageEntity:
        """
        Converts GamesGetPageDto object to GamesGetPageEntity object.

        Parameters:
        - dto: GamesGetPageDto object.

        Returns:
        - GamesGetPageEntity: GamesGetPageEntity object.
        """
        return GamesGetPageEntity(
            page=dto.page,
            search=dto.search,
            sort_field=dto.sort_field,
            sort_direction=dto.sort_direction,
            limit=dto.limit
        )

    def create_dto_to_entity(
        self,
        dto: GameCreateDto
    ) -> GameCreateEntity:
        """
        Converts GameCreateDto object to GameCreateEntity object.

        Parameters:
        - dto: GameCreateDto object.

        Returns:
        - GameCreateEntity: GameCreateEntity object.
        """
        return GameCreateEntity(
            name=GameName(dto.name)
        )

    def update_dto_to_entity(
        self,
        game_id: int,
        dto: GameUpdateDto
    ) -> GameUpdateEntity:
        """
        Converts GameUpdateDto object to GameUpdateEntity object.

        Parameters:
        - game_id: Game ID.
        - dto: GameUpdateDto object.

        Returns:
        - GameUpdateEntity: GameUpdateEntity object.
        """
        return GameUpdateEntity(
            id=game_id,
            name=GameName(dto.name)
        )
