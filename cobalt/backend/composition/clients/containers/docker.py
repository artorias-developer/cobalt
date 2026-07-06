#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.managers import AbstractI18nManager
from application.contracts.clients import AbstractContainersClient
from infrastructure.clients.containers.docker import DockerClient


def create_docker_client(
    i18n_manager: AbstractI18nManager
) -> AbstractContainersClient:
    """
    Creates a Docker client.

    Parameters:
    - i18n_manager: AbstractI18nManager object.

    Returns:
    - AbstractContainersClient: AbstractContainersClient object.
    """
    return DockerClient(
        i18n_manager=i18n_manager
    )
