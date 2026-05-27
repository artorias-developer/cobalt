#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.clients import AbstractContainersClient
from infrastructure.clients.containers.docker import DockerClient


def create_docker_client() -> AbstractContainersClient:
    """
    Creates a Docker client.

    Parameters:
    - None.

    Returns:
    - AbstractContainersClient: AbstractContainersClient object.
    """
    return DockerClient()
