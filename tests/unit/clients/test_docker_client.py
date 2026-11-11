#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

"""
Host ports collection of the Docker client.

The Docker Engine API is replaced with an autospec socket client that answers "/containers/json".
"""

from typing import Any, Dict, List, Optional
from unittest.mock import create_autospec

import pytest
from orjson import dumps

from domain.exceptions import UnexpectedError
from application.contracts.clients import AbstractSocketClient
from application.clients.sockets.shared import SocketResponse
from infrastructure.clients.containers.docker import DockerClient


PORTS_LABEL = "cobalt_ports"


def _container(
    state: str,
    ports_label: Optional[str] = None,
    public_ports: Optional[List[Optional[int]]] = None
) -> Dict[str, Any]:
    return {
        "Id": "id",
        "State": state,
        "Labels": {PORTS_LABEL: ports_label} if ports_label is not None else {},
        "Ports": [
            {"PrivatePort": 1, "Type": "tcp", **({"PublicPort": port} if port else {})}
            for port in public_ports or []
        ]
    }


@pytest.fixture
def docker():
    """
    Returns a factory: docker(containers, status) -> (client, socket_client).
    """
    def make(containers: List[Dict[str, Any]], status: int = 200):
        socket_client = create_autospec(AbstractSocketClient, instance=True)
        socket_client.request.return_value = SocketResponse(status=status, body=dumps(containers))

        return DockerClient(socket_client=socket_client), socket_client

    return make


class TestContainersHostPorts:
    async def test_makes_single_request_for_all_containers(self, docker):
        client, socket_client = docker([
            _container("running", public_ports=[25565]),
            _container("exited", ports_label="40000"),
            _container("created", ports_label="40010")
        ])

        await client.used_ports_by_label(ports_label=PORTS_LABEL)

        socket_client.request.assert_awaited_once()
        assert socket_client.request.await_args.kwargs["path"] == "/containers/json"
        assert socket_client.request.await_args.kwargs["params"] == {"all": True}

    async def test_running_ports_are_taken_from_list(self, docker):
        client, _ = docker([
            _container("running", public_ports=[25565, 25565, None]),
            _container("running", public_ports=[7777])
        ])

        assert await client.used_ports_by_label(ports_label=PORTS_LABEL) == {25565, 7777}

    async def test_stopped_ports_are_taken_from_label(self, docker):
        client, _ = docker([
            _container("exited", ports_label="40000"),
            _container("created", ports_label="40010,40011,40012")
        ])

        assert await client.used_ports_by_label(ports_label=PORTS_LABEL) == {40000, 40010, 40011, 40012}

    async def test_published_and_label_ports_are_merged(self, docker):
        client, _ = docker([
            _container("running", ports_label="40000,40001", public_ports=[40000, 40001]),
            _container("exited", ports_label="40010"),
            _container("running", public_ports=[443])
        ])

        assert await client.used_ports_by_label(ports_label=PORTS_LABEL) == {40000, 40001, 40010, 443}

    async def test_stopped_without_label_is_ignored(self, docker):
        client, _ = docker([
            _container("exited"),
            {"Id": "bare", "State": "exited"}
        ])

        assert await client.used_ports_by_label(ports_label=PORTS_LABEL) == set()

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("", set()),
            (",", set()),
            ("abc", set()),
            ("40000,,abc, 40001 ", {40000, 40001})
        ]
    )
    async def test_malformed_label_values_are_skipped(self, docker, value, expected):
        client, _ = docker([_container("exited", ports_label=value)])

        assert await client.used_ports_by_label(ports_label=PORTS_LABEL) == expected

    async def test_list_failure_is_raised(self, docker):
        client, _ = docker([], status=500)

        with pytest.raises(UnexpectedError):
            await client.used_ports_by_label(ports_label=PORTS_LABEL)
