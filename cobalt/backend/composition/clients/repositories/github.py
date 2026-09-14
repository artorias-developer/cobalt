#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.clients import (
    AbstractRepositoriesClient,
    AbstractHttpClient
)
from application.contracts.loggers import AbstractLogger
from infrastructure.clients import GithubClient


def create_github_client(
    http_client: AbstractHttpClient,
    logger: AbstractLogger
) -> AbstractRepositoriesClient:
    """
    Creates a GitHub client.

    Parameters:
    - http_client: AbstractHttpClient object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractCacheClient: AbstractCacheClient object.
    """
    return GithubClient(
        http_client=http_client,
        logger=logger
    )
