#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

"""
Shared fixtures for unit tests.

All external dependencies (cache, repositories, hasher, WebSocket connections, i18n, logger)
are replaced with autospec mocks, so method names and signatures are checked against the contracts.
"""

from collections import defaultdict
from typing import Any
from unittest.mock import AsyncMock, MagicMock, create_autospec, sentinel

import pytest

from domain.repositories import (
    AbstractRolesRepository,
    AbstractServersRepository,
    AbstractUsersRepository
)
from application.contracts.clients import (
    AbstractCacheClient,
    AbstractContainersClient,
    AbstractMetricsClient
)
from application.contracts.queues import AbstractQueue
from application.contracts.managers import (
    AbstractConnectionsManager,
    AbstractI18nManager
)
from application.contracts.hashers import AbstractHasher
from application.contracts.loggers import AbstractLogger
from application.contracts.services import (
    AbstractAttributesService,
    AbstractAuthService,
    AbstractFilesService,
    AbstractGamesService,
    AbstractLoadersService,
    AbstractLogsService,
    AbstractMetricsService,
    AbstractRolesService,
    AbstractServersService,
    AbstractSettingsService,
    AbstractUsersService
)


def _format_pattern(pattern: str, **kwargs: Any) -> str:
    # Mirrors RedisCacheClient.format_pattern: missing placeholders become "*".
    return pattern.format_map(defaultdict(lambda: "*", **kwargs))


@pytest.fixture
def cache_client() -> MagicMock:
    mock = create_autospec(AbstractCacheClient, instance=True)
    mock.format_pattern.side_effect = _format_pattern
    mock.get.return_value = None
    return mock


@pytest.fixture
def connections_manager() -> MagicMock:
    mock = create_autospec(AbstractConnectionsManager, instance=True)
    mock.get_connections.return_value = {}
    return mock


@pytest.fixture
def hasher() -> MagicMock:
    mock = create_autospec(AbstractHasher, instance=True)
    mock.generate_salt.return_value = "generated_salt"
    mock.hash.return_value = "generated_hash"
    mock.verify.return_value = True
    return mock


@pytest.fixture
def i18n_manager() -> MagicMock:
    mock = create_autospec(AbstractI18nManager, instance=True)
    mock.gettext.side_effect = lambda message, *args, **kwargs: message
    return mock


@pytest.fixture
def logger() -> MagicMock:
    return create_autospec(AbstractLogger, instance=True)


@pytest.fixture
def containers_client() -> MagicMock:
    return create_autospec(AbstractContainersClient, instance=True)


@pytest.fixture
def metrics_client() -> MagicMock:
    return create_autospec(AbstractMetricsClient, instance=True)


@pytest.fixture
def queue() -> MagicMock:
    return create_autospec(AbstractQueue, instance=True)


@pytest.fixture
def transactions_manager() -> MagicMock:
    """
    Async context manager whose `session` is a sentinel; exceptions inside the block propagate.
    """
    mock = MagicMock()
    mock.session = sentinel.session
    mock.__aenter__ = AsyncMock(return_value=mock)
    mock.__aexit__ = AsyncMock(return_value=False)
    return mock


@pytest.fixture
def servers_repository() -> MagicMock:
    return create_autospec(AbstractServersRepository, instance=True)


@pytest.fixture
def loaders_service_mock() -> MagicMock:
    return create_autospec(AbstractLoadersService, instance=True)


@pytest.fixture
def roles_repository() -> MagicMock:
    return create_autospec(AbstractRolesRepository, instance=True)


@pytest.fixture
def users_repository() -> MagicMock:
    return create_autospec(AbstractUsersRepository, instance=True)


@pytest.fixture
def roles_service_mock() -> MagicMock:
    return create_autospec(AbstractRolesService, instance=True)


@pytest.fixture
def users_service_mock() -> MagicMock:
    return create_autospec(AbstractUsersService, instance=True)


@pytest.fixture
def auth_service_mock() -> MagicMock:
    mock = create_autospec(AbstractAuthService, instance=True)
    mock.get_session_user.return_value = None
    return mock


@pytest.fixture
def attributes_service_mock() -> MagicMock:
    return create_autospec(AbstractAttributesService, instance=True)


@pytest.fixture
def files_service_mock() -> MagicMock:
    return create_autospec(AbstractFilesService, instance=True)


@pytest.fixture
def games_service_mock() -> MagicMock:
    return create_autospec(AbstractGamesService, instance=True)


@pytest.fixture
def logs_service_mock() -> MagicMock:
    return create_autospec(AbstractLogsService, instance=True)


@pytest.fixture
def metrics_service_mock() -> MagicMock:
    return create_autospec(AbstractMetricsService, instance=True)


@pytest.fixture
def servers_service_mock() -> MagicMock:
    return create_autospec(AbstractServersService, instance=True)


@pytest.fixture
def settings_service_mock() -> MagicMock:
    return create_autospec(AbstractSettingsService, instance=True)
