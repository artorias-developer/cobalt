#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.clients import AbstractSocketClient
from infrastructure.clients import UnixSocketClient
from infrastructure.configs import ApplicationConfig


def create_unix_socket_client(
    config: ApplicationConfig
) -> AbstractSocketClient:
    """
    Creates a Aiohttp client.

    Parameters:
    - config: ApplicationConfig object.

    Returns:
    - AbstractHttpClient: AbstractHttpClient object.
    """
    return UnixSocketClient(
        socket_path=config.containers.socket_path,
        base_url=config.containers.base_url
    )
