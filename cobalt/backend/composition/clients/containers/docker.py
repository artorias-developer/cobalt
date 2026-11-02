#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.clients import (
    AbstractContainersClient,
    AbstractSocketClient
)
from infrastructure.clients import DockerClient
from infrastructure.configs import ApplicationConfig


def create_docker_client(
    config: ApplicationConfig,
    socket_client: AbstractSocketClient
) -> AbstractContainersClient:
    """
    Creates a Docker client.

    Parameters:
    - config: ApplicationConfig object.
    - socket_client: AbstractSocketClient object.

    Returns:
    - AbstractContainersClient: AbstractContainersClient object.
    """
    return DockerClient(
        socket_client=socket_client,
        socket_path=config.containers.socket_path,
        docker_cli=config.containers.cli_path
    )
