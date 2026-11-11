#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

"""
End-to-end WebSocket tests through TestClient: connection, auth, dispatch, permissions and errors.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import pytest
from starlette.websockets import WebSocketDisconnect

from domain.enums import PermissionEnum
from domain.exceptions import ConflictError, NotFoundError
from application.dtos import (
    LogsSubscribeServerDto,
    LogsUnsubscribeServerDto,
    MetricsSubscribeServerDto,
    MetricsUnsubscribeServerDto
)
from application.managers.events.shared import (
    LogEventEnum,
    MetricEventEnum,
    ServerEventEnum
)
from presentation.ws.shared import WebSocketStatusCodesEnum

from helpers.routes import all_permissions_except
from helpers.ws import WS_URL, collect_replies, send_event, sync


USER_ID = 7


@dataclass(frozen=True)
class WsEvent:
    event: str
    service: str
    method: str
    permissions: List[PermissionEnum]
    data: Optional[Dict[str, Any]] = None
    extra_kwargs: Dict[str, Any] = field(default_factory=dict)

    @property
    def id(self) -> str:
        return self.event


def _server_event(event, service, method, permission, dto_cls) -> WsEvent:
    return WsEvent(
        event=event, service=service, method=method, permissions=[permission],
        data={"server_id": 3}, extra_kwargs={"dto": dto_cls(server_id=3)}
    )


EVENTS = [
    WsEvent(LogEventEnum.SUBSCRIBE_HOST, "logs", "subscribe_host", [PermissionEnum.DASHBOARD_LOGS_VIEW]),
    WsEvent(LogEventEnum.UNSUBSCRIBE_HOST, "logs", "unsubscribe_host", [PermissionEnum.DASHBOARD_LOGS_VIEW]),
    _server_event(LogEventEnum.SUBSCRIBE_SERVER, "logs", "subscribe_server",
                  PermissionEnum.SERVER_LOGS_VIEW, LogsSubscribeServerDto),
    _server_event(LogEventEnum.UNSUBSCRIBE_SERVER, "logs", "unsubscribe_server",
                  PermissionEnum.SERVER_LOGS_VIEW, LogsUnsubscribeServerDto),

    WsEvent(MetricEventEnum.SUBSCRIBE_HOST_CPU, "metrics", "subscribe_host_cpu", [PermissionEnum.DASHBOARD_CPU_VIEW]),
    WsEvent(MetricEventEnum.UNSUBSCRIBE_HOST_CPU, "metrics", "unsubscribe_host_cpu", [PermissionEnum.DASHBOARD_CPU_VIEW]),
    WsEvent(MetricEventEnum.SUBSCRIBE_HOST_RAM, "metrics", "subscribe_host_ram", [PermissionEnum.DASHBOARD_RAM_VIEW]),
    WsEvent(MetricEventEnum.UNSUBSCRIBE_HOST_RAM, "metrics", "unsubscribe_host_ram", [PermissionEnum.DASHBOARD_RAM_VIEW]),
    _server_event(MetricEventEnum.SUBSCRIBE_SERVER_CPU, "metrics", "subscribe_server_cpu",
                  PermissionEnum.SERVER_CPU_VIEW, MetricsSubscribeServerDto),
    _server_event(MetricEventEnum.UNSUBSCRIBE_SERVER_CPU, "metrics", "unsubscribe_server_cpu",
                  PermissionEnum.SERVER_CPU_VIEW, MetricsUnsubscribeServerDto),
    _server_event(MetricEventEnum.SUBSCRIBE_SERVER_RAM, "metrics", "subscribe_server_ram",
                  PermissionEnum.SERVER_RAM_VIEW, MetricsSubscribeServerDto),
    _server_event(MetricEventEnum.UNSUBSCRIBE_SERVER_RAM, "metrics", "unsubscribe_server_ram",
                  PermissionEnum.SERVER_RAM_VIEW, MetricsUnsubscribeServerDto),

    WsEvent(ServerEventEnum.SUBSCRIBE_STATES, "servers", "subscribe_states", [PermissionEnum.SERVERS_VIEW]),
    WsEvent(ServerEventEnum.UNSUBSCRIBE_STATES, "servers", "unsubscribe_states", [PermissionEnum.SERVERS_VIEW])
]


@pytest.fixture
def services(logs_service_mock, metrics_service_mock, servers_service_mock):
    return {
        "logs": logs_service_mock,
        "metrics": metrics_service_mock,
        "servers": servers_service_mock
    }


class TestConnection:
    def test_without_session_is_rejected_with_4401(self, ws_client, connections_manager):
        with pytest.raises(WebSocketDisconnect) as exc_info:
            with ws_client.websocket_connect(WS_URL):
                pass

        assert exc_info.value.code == WebSocketStatusCodesEnum.WS_4401_UNAUTHORIZED
        connections_manager.register.assert_not_awaited()

    def test_expired_session_is_rejected(self, ws_client, auth_service_mock):
        ws_client.cookies.set("session_id", "expired")
        auth_service_mock.get_session_user.return_value = None

        with pytest.raises(WebSocketDisconnect) as exc_info:
            with ws_client.websocket_connect(WS_URL):
                pass

        assert exc_info.value.code == WebSocketStatusCodesEnum.WS_4401_UNAUTHORIZED
        auth_service_mock.get_session_user.assert_awaited_once_with(session_id="expired")

    def test_auth_backend_failure_is_rejected_not_crashed(self, ws_client, auth_service_mock):
        ws_client.cookies.set("session_id", "abc")
        auth_service_mock.get_session_user.side_effect = ConnectionError("redis down")

        with pytest.raises(WebSocketDisconnect) as exc_info:
            with ws_client.websocket_connect(WS_URL):
                pass

        assert exc_info.value.code == WebSocketStatusCodesEnum.WS_4401_UNAUTHORIZED

    def test_registers_and_unregisters_connection_by_user_id(self, ws_client, ws_login_as, connections_manager):
        ws_login_as(ws_client, user_id=USER_ID)

        with ws_client.websocket_connect(WS_URL) as websocket:
            sync(websocket)
            connections_manager.register.assert_awaited_once()
            assert connections_manager.register.await_args.kwargs["connection_id"] == USER_ID
            connections_manager.unregister.assert_not_awaited()

        connections_manager.unregister.assert_awaited_once_with(connection_id=USER_ID)


class TestEventsDispatch:
    @pytest.mark.parametrize("case", EVENTS, ids=[case.id for case in EVENTS])
    def test_event_calls_service_with_connection_id(self, ws_client, ws_login_as, services, case):
        ws_login_as(ws_client, permissions=case.permissions, user_id=USER_ID)
        method = getattr(services[case.service], case.method)

        with ws_client.websocket_connect(WS_URL) as websocket:
            send_event(websocket, case.event, case.data)
            sync(websocket)

        method.assert_awaited_once_with(connection_id=USER_ID, **case.extra_kwargs)

    @pytest.mark.parametrize("case", EVENTS, ids=[case.id for case in EVENTS])
    def test_event_without_permission_returns_4403(self, ws_client, ws_login_as, services, case):
        ws_login_as(ws_client, permissions=all_permissions_except(case.permissions))
        method = getattr(services[case.service], case.method)

        with ws_client.websocket_connect(WS_URL) as websocket:
            send_event(websocket, case.event, case.data)
            [reply] = collect_replies(websocket)

        assert reply == {
            "type": "error",
            "code": WebSocketStatusCodesEnum.WS_4403_FORBIDDEN,
            "data": "Not enough permissions"
        }
        method.assert_not_awaited()


class TestErrors:
    def test_unknown_event_returns_4400_and_keeps_connection(self, ws_client, ws_login_as, servers_service_mock):
        ws_login_as(ws_client)

        with ws_client.websocket_connect(WS_URL) as websocket:
            send_event(websocket, "does_not_exist")
            [reply] = collect_replies(websocket)

            # Connection is still usable after the error.
            send_event(websocket, ServerEventEnum.SUBSCRIBE_STATES)
            sync(websocket)

        assert reply == {
            "type": "error",
            "code": WebSocketStatusCodesEnum.WS_4400_BAD_REQUEST,
            "data": 'Unknown event "does_not_exist"'
        }
        servers_service_mock.subscribe_states.assert_awaited_once()

    def test_message_without_event_returns_4400(self, ws_client, ws_login_as):
        ws_login_as(ws_client)

        with ws_client.websocket_connect(WS_URL) as websocket:
            websocket.send_json({"data": {}})
            [reply] = collect_replies(websocket)

        assert reply["code"] == WebSocketStatusCodesEnum.WS_4400_BAD_REQUEST

    @pytest.mark.parametrize("data", [None, {}, {"server_id": "abc"}])
    def test_invalid_payload_returns_4400(self, ws_client, ws_login_as, logs_service_mock, data):
        ws_login_as(ws_client)

        with ws_client.websocket_connect(WS_URL) as websocket:
            send_event(websocket, LogEventEnum.SUBSCRIBE_SERVER, data)
            [reply] = collect_replies(websocket)

        assert reply["type"] == "error"
        assert reply["code"] == WebSocketStatusCodesEnum.WS_4400_BAD_REQUEST
        assert "server_id" in reply["data"]
        logs_service_mock.subscribe_server.assert_not_awaited()

    @pytest.mark.parametrize(
        ("error", "code", "message"),
        [
            (NotFoundError("Server {server_id} not found", server_id=3),
             WebSocketStatusCodesEnum.WS_4404_NOT_FOUND, "Server 3 not found"),
            (ConflictError("Already subscribed"),
             WebSocketStatusCodesEnum.WS_4409_CONFLICT, "Already subscribed")
        ]
    )
    def test_domain_errors_from_service_are_reported(
        self, ws_client, ws_login_as, metrics_service_mock, error, code, message
    ):
        ws_login_as(ws_client)
        metrics_service_mock.subscribe_server_cpu.side_effect = error

        with ws_client.websocket_connect(WS_URL) as websocket:
            send_event(websocket, MetricEventEnum.SUBSCRIBE_SERVER_CPU, {"server_id": 3})
            [reply] = collect_replies(websocket)

        assert reply == {"type": "error", "code": code, "data": message}

    def test_unexpected_error_is_hidden_and_logged(self, ws_client, ws_login_as, servers_service_mock, logger):
        ws_login_as(ws_client)
        servers_service_mock.subscribe_states.side_effect = RuntimeError("secret internals")

        with ws_client.websocket_connect(WS_URL) as websocket:
            send_event(websocket, ServerEventEnum.SUBSCRIBE_STATES)
            [reply] = collect_replies(websocket)

        assert reply == {
            "type": "error",
            "code": WebSocketStatusCodesEnum.WS_1011_INTERNAL_SERVER_ERROR,
            "data": "Internal server error"
        }
        logger.exception.assert_called_once()

    def test_connection_is_unregistered_after_errors(self, ws_client, ws_login_as, servers_service_mock, connections_manager):
        ws_login_as(ws_client, user_id=USER_ID)
        servers_service_mock.subscribe_states.side_effect = RuntimeError("boom")

        with ws_client.websocket_connect(WS_URL) as websocket:
            send_event(websocket, ServerEventEnum.SUBSCRIBE_STATES)
            collect_replies(websocket)

        connections_manager.unregister.assert_awaited_once_with(connection_id=USER_ID)
