#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from enum import StrEnum
from inspect import signature, iscoroutine
from typing import Callable, Any, Dict, List, Optional

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError

from domain.exceptions import ValidationError
from application.dtos import UserDto
from application.contracts.managers import (
    AbstractEventsManager,
    AbstractConnectionsManager, AbstractI18nManager
)


class EventsManager(AbstractEventsManager):
    """
    WebSockets events manager.
    """
    connections_manager: AbstractConnectionsManager
    i18n_manager: AbstractI18nManager

    _: Callable

    def __init__(
        self,
        connections_manager: AbstractConnectionsManager,
        i18n_manager: AbstractI18nManager
    ):
        super().__init__()

        self.connections_manager = connections_manager
        self.i18n_manager = i18n_manager

        self._ = i18n_manager.gettext

    @staticmethod
    async def _call_with_context(
        func: Callable,
        context: Dict[str, Any]
    ) -> Any:
        """
        Executes a function with parameters automatically injected from context.

        Parameters:
        - func: Callable to be executed.
        - context: Dictionary with available context values.

        Returns:
        - Any: Result of the function execution.
        """
        func_kwargs = {
            param_name: context[param_name]
            for param_name in signature(func).parameters.keys()
            if param_name in context
        }

        result = func(**func_kwargs)

        if iscoroutine(result):
            result = await result

        return result

    async def execute_event_dependencies(
        self,
        dependencies: List[Callable],
        context: Dict[str, Any]
    ) -> None:
        """
        Runs event dependencies in order.

        Parameters:
        - dependencies: List of callables to be executed.
        - context: Dictionary with available context values.

        Returns:
        - None.
        """
        for dependency in dependencies:
            if hasattr(dependency, "dependency"):
                await self._call_with_context(dependency.dependency, context)

    async def resolve_handler_dependencies(
        self,
        handler: Callable,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Resolves arguments in the handler.

        Parameters:
        - handler: Callable function (the event handler).
        - context: Dictionary with available context values.

        Returns:
        - Dict: Dictionary with the resolved arguments.
        """
        kwargs = {}

        for name, param in signature(handler).parameters.items():
            if hasattr(param.default, "dependency"):
                kwargs[name] = await self._call_with_context(param.default.dependency, context)
                continue

            try:
                is_model = isinstance(param.annotation, type) and issubclass(param.annotation, BaseModel)
            except TypeError:
                is_model = False

            if name in context:
                value = context[name]
                if is_model and not isinstance(value, param.annotation):
                    kwargs[name] = param.annotation.from_dict(value)
                else:
                    kwargs[name] = value
                continue

            if is_model:
                try:
                    kwargs[name] = param.annotation.from_dict(context.get("data", {}))
                except PydanticValidationError as e:
                    raise ValidationError(str(e)) from e

        return kwargs

    async def handler(
        self,
        websocket: WebSocket
    ) -> None:
        """
        Handles WebSockets events.

        Parameters:
        - websocket: WebSockets object.

        Returns:
        - None.
        """
        await websocket.accept()

        user = websocket.state.user
        connection_id = user.id

        await self.connections_manager.register(
            connection_id=connection_id,
            connection=websocket
        )

        try:
            async for message in websocket.iter_json():
                event = message.get("event")
                data = message.get("data", {})

                await self.dispatch_event(
                    event=event,
                    data=data,
                    websocket=websocket,
                    connection_id=connection_id,
                    user=user
                )
        except WebSocketDisconnect:
            pass

        finally:
            await self.connections_manager.unregister(
                connection_id=connection_id
            )

    def on_event(
        self,
        event: StrEnum,
        handler: Callable,
        dependencies: Optional[List[Callable]] = None
    ) -> None:
        """
        Registers event handler.

        Parameters:
        - event: Event name.
        - handler: Callable to be executed.
        - dependencies: Dependencies to be executed.

        Returns:
        - None.
        """
        self._event_handlers[event] = {
            "handler": handler,
            "dependencies": dependencies or []
        }

    async def dispatch_event(
        self,
        event: StrEnum,
        data: Any,
        websocket: WebSocket,
        connection_id: int,
        user: UserDto
    ) -> None:
        """
        Calls registered event handler.

        Parameters:
        - event: Event name.
        - data: Data to be processed.
        - websocket: WebSockets object.
        - connection_id: Connection ID.
        - user: UserDto object.

        Returns:
        - None.
        """
        context = {
            "websocket": websocket,
            "connection_id": connection_id,
            "event": event,
            "data": data,
            "user": user
        }

        async def _dispatch() -> None:
            if event not in self._event_handlers:
                raise ValidationError(self._('Unknown event "{event}"').format(event=event))

            event_data = self._event_handlers[event]

            await self.execute_event_dependencies(
                dependencies=event_data["dependencies"],
                context=context
            )

            handler_kwargs = await self.resolve_handler_dependencies(
                handler=event_data["handler"],
                context=context
            )

            await event_data["handler"](**handler_kwargs)

        chain = _dispatch

        for interceptor in reversed(self._interceptors):
            current_interceptor = interceptor
            current_chain = chain

            async def call_next_wrapper(m=current_interceptor, c=current_chain) -> None:
                await m.dispatch(c, websocket=websocket)

            chain = call_next_wrapper

        await chain()