#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from composition.dataclasses import MappersContainer

from .repositories import create_postgres_repositories_mappers
from .routers import create_fastapi_routers_mappers
from .services import create_services_mappers

__all__ = [
    "create_fastapi_postgres_mappers_container"
]


def create_fastapi_postgres_mappers_container() -> MappersContainer:
    """
    Creates a FastAPI + Postgres mappers container.

    Parameters:
    - None.

    Returns:
    - MappersContainer: MappersContainer object.
    """
    repositories_mappers = create_postgres_repositories_mappers()
    services_mappers = create_services_mappers()
    routers_mappers = create_fastapi_routers_mappers()

    return MappersContainer(
        repositories=repositories_mappers,
        services=services_mappers,
        routers=routers_mappers
    )