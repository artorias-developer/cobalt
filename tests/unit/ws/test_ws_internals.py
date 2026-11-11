#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

"""
Unit tests for EventsManager dispatching and WsErrorsInterceptor, without a real socket.
"""

from enum import StrEnum
from typing import List
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import Depends, WebSocketException, status
from pydantic import ValidationError as PydanticValidationError
from starlette.websockets import WebSocketState

from domain.enums import PermissionEnum
from domain.exceptions import (
    BaseError,
    UnexpectedError,
    ValidationError,
    AuthenticationError,
    PermissionsError,
    NotFoundError,
    ConflictError
)
from application.dtos import LogsSubscribeServerDto
from presentation.ws.fastapi.v1.interceptors import WsErrorsInterceptor
from presentation.ws.fastapi.v1.managers import EventsManager
from presentation.ws.fastapi.v1.routers import BaseWsRouter
from presentation.ws.shared import WebSocketStatusCodesEnum

from helpers.factories import make_role_dto, make_user_dto


class TestEvent(StrEnum):
    __test__ = False

    PING = "ping"


def _fake_websocket(state: WebSocketState = WebSocketState.CONNECTED) -> MagicMock:
    websocket = MagicMock()
    websocket.client_state = state
    websocket.send_json = AsyncMock()
    return websocket


@pytest.fixture
def manager(connections_manager) -> EventsManager:
    return EventsManager(connections_manager=connections_manager)


async def _dispatch(manager, event=TestEvent.PING, data=None, websocket=None, user=None):
    await manager.dispatch_event(
        event=event,
        data=data if data is not None else {},
        websocket=websocket or _fake_websocket(),
        connection_id=1,
        user=user or make_user_dto()
    )


class TestEventsManagerDispatch:
    async def test_unknown_event_raises_validation_error(self, manager):
        with pytest.raises(ValidationError) as exc_info:
            await _dispatch(manager, event="missing")

        assert exc_info.value.kwargs == {"event": "missing"}

    async def test_injects_context_by_parameter_name(self, manager):
        received = {}
        user = make_user_dto(user_id=5)

        async def handler(connection_id: int, user, event):
            received.update(connection_id=connection_id, user=user, event=event)

        manager.on_event(event=TestEvent.PING, handler=handler)
        await _dispatch(manager, user=user)

        assert received == {"connection_id": 1, "user": user, "event": TestEvent.PING}

    async def test_builds_dto_from_event_data(self, manager):
        handler = AsyncMock()

        async def typed_handler(dto: LogsSubscribeServerDto):
            await handler(dto)

        manager.on_event(event=TestEvent.PING, handler=typed_handler)
        await _dispatch(manager, data={"server_id": 9})

        handler.assert_awaited_once_with(LogsSubscribeServerDto(server_id=9))

    async def test_invalid_event_data_raises_pydantic_error(self, manager):
        async def typed_handler(dto: LogsSubscribeServerDto):
            ...

        manager.on_event(event=TestEvent.PING, handler=typed_handler)

        with pytest.raises(PydanticValidationError):
            await _dispatch(manager, data={"server_id": "nope"})

    async def test_dependencies_run_before_handler_and_can_block_it(self, manager):
        calls: List[str] = []
        handler = AsyncMock(side_effect=lambda: calls.append("handler"))

        def blocking_dependency(user):
            calls.append(f"dependency:{user.id}")
            raise PermissionsError("Not enough permissions")

        manager.on_event(event=TestEvent.PING, handler=handler, dependencies=[Depends(blocking_dependency)])

        with pytest.raises(PermissionsError):
            await _dispatch(manager)

        assert calls == ["dependency:1"]
        handler.assert_not_awaited()

    async def test_sync_and_async_dependencies_are_supported(self, manager):
        calls: List[str] = []

        def sync_dependency():
            calls.append("sync")

        async def async_dependency():
            calls.append("async")

        manager.on_event(
            event=TestEvent.PING,
            handler=AsyncMock(),
            dependencies=[Depends(sync_dependency), Depends(async_dependency)]
        )
        await _dispatch(manager)

        assert calls == ["sync", "async"]

    async def test_interceptors_wrap_in_registration_order(self, manager):
        calls: List[str] = []

        class Recorder:
            def __init__(self, name):
                self.name = name

            async def dispatch(self, call_next, **kwargs):
                calls.append(f"{self.name}:before")
                await call_next()
                calls.append(f"{self.name}:after")

        manager.add_interceptor(Recorder("outer"))
        manager.add_interceptor(Recorder("inner"))
        manager.on_event(event=TestEvent.PING, handler=AsyncMock(side_effect=lambda: calls.append("handler")))

        await _dispatch(manager)

        assert calls == ["outer:before", "inner:before", "handler", "inner:after", "outer:after"]

    async def test_errors_interceptor_turns_exception_into_error_message(self, manager, i18n_manager, logger):
        websocket = _fake_websocket()
        manager.add_interceptor(WsErrorsInterceptor(i18n_manager=i18n_manager, logger=logger))

        await _dispatch(manager, event="missing", websocket=websocket)

        websocket.send_json.assert_awaited_once_with({
            "type": "error",
            "code": WebSocketStatusCodesEnum.WS_4400_BAD_REQUEST,
            "data": 'Unknown event "missing"'
        })


class UnmappedError(BaseError):
    ...


@pytest.fixture
def interceptor(i18n_manager, logger) -> WsErrorsInterceptor:
    return WsErrorsInterceptor(i18n_manager=i18n_manager, logger=logger)


class TestWsErrorsInterceptor:
    @pytest.mark.parametrize(
        ("error", "code"),
        [
            (UnexpectedError("x"), WebSocketStatusCodesEnum.WS_1011_INTERNAL_SERVER_ERROR),
            (ValidationError("x"), WebSocketStatusCodesEnum.WS_4400_BAD_REQUEST),
            (AuthenticationError("x"), WebSocketStatusCodesEnum.WS_4401_UNAUTHORIZED),
            (PermissionsError("x"), WebSocketStatusCodesEnum.WS_4403_FORBIDDEN),
            (NotFoundError("x"), WebSocketStatusCodesEnum.WS_4404_NOT_FOUND),
            (ConflictError("x"), WebSocketStatusCodesEnum.WS_4409_CONFLICT)
        ]
    )
    async def test_maps_domain_errors(self, interceptor, error, code):
        websocket = _fake_websocket()

        await interceptor.dispatch(AsyncMock(side_effect=error), websocket=websocket)

        websocket.send_json.assert_awaited_once_with({"type": "error", "code": code, "data": "x"})

    async def test_message_is_translated_then_formatted(self, interceptor, i18n_manager):
        i18n_manager.gettext.side_effect = lambda message: f"[uk] {message}"
        websocket = _fake_websocket()

        await interceptor.dispatch(
            AsyncMock(side_effect=NotFoundError("Server {server_id} not found", server_id=3)),
            websocket=websocket
        )

        assert websocket.send_json.await_args.args[0]["data"] == "[uk] Server 3 not found"

    async def test_unmapped_base_error_is_1011_with_warning(self, interceptor, logger):
        websocket = _fake_websocket()

        await interceptor.dispatch(AsyncMock(side_effect=UnmappedError("boom")), websocket=websocket)

        assert websocket.send_json.await_args.args[0]["code"] == status.WS_1011_INTERNAL_ERROR
        logger.warning.assert_called_once()

    async def test_pydantic_error_is_4400(self, interceptor):
        websocket = _fake_websocket()

        try:
            LogsSubscribeServerDto.from_dict({})
        except PydanticValidationError as e:
            error = e

        await interceptor.dispatch(AsyncMock(side_effect=error), websocket=websocket)

        message = websocket.send_json.await_args.args[0]
        assert message["code"] == WebSocketStatusCodesEnum.WS_4400_BAD_REQUEST
        assert "server_id" in message["data"]

    async def test_unknown_exception_is_hidden_and_logged(self, interceptor, logger):
        websocket = _fake_websocket()

        await interceptor.dispatch(AsyncMock(side_effect=KeyError("secret")), websocket=websocket)

        assert websocket.send_json.await_args.args[0]["data"] == "Internal server error"
        logger.exception.assert_called_once()

    @pytest.mark.parametrize("state", [WebSocketState.CONNECTING, WebSocketState.DISCONNECTED])
    async def test_does_not_send_to_closed_socket(self, interceptor, state):
        websocket = _fake_websocket(state)

        await interceptor.dispatch(AsyncMock(side_effect=NotFoundError("x")), websocket=websocket)

        websocket.send_json.assert_not_awaited()

    async def test_without_websocket_swallows_error(self, interceptor):
        await interceptor.dispatch(AsyncMock(side_effect=NotFoundError("x")))

    async def test_success_sends_nothing(self, interceptor):
        websocket = _fake_websocket()
        call_next = AsyncMock()

        await interceptor.dispatch(call_next, websocket=websocket)

        call_next.assert_awaited_once()
        websocket.send_json.assert_not_awaited()


class TestBaseWsRouter:
    @pytest.fixture
    def router(self, auth_service_mock) -> BaseWsRouter:
        return BaseWsRouter(auth_service=auth_service_mock)

    async def test_session_required_rejects_with_4401(self, router):
        websocket = MagicMock()
        websocket.state.user = None

        with pytest.raises(WebSocketException) as exc_info:
            await router.session_required(websocket)

        assert exc_info.value.code == WebSocketStatusCodesEnum.WS_4401_UNAUTHORIZED

    async def test_permission_dependency(self, router):
        dependency = router.one_of_permissions_required([PermissionEnum.SERVERS_VIEW, PermissionEnum.SERVER_VIEW])
        websocket = MagicMock()

        websocket.state.user = make_user_dto(role=make_role_dto(permissions=[PermissionEnum.SERVER_VIEW]))
        assert await dependency(websocket) is websocket.state.user

        websocket.state.user = make_user_dto(role=make_role_dto(permissions=[]))
        with pytest.raises(PermissionsError):
            await dependency(websocket)

        websocket.state.user = None
        with pytest.raises(AuthenticationError):
            await dependency(websocket)
