#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional, Dict, Any, Literal, AsyncGenerator

from aiohttp import ClientSession, ClientTimeout, ClientError, UnixConnector

from application.contracts.clients import AbstractSocketClient
from application.clients.sockets.shared import (
    SocketError,
    SocketResponse
)


class UnixSocketClient(AbstractSocketClient):
    """
    Aiohttp HTTP client over a unix domain socket.
    """
    _session: Optional[ClientSession]

    socket_path: str
    base_url: str

    def __init__(
        self,
        socket_path: str,
        base_url: str
    ):
        self.socket_path = socket_path
        self.base_url = base_url.rstrip("/")

        self._session = None

    def _get_session(self) -> ClientSession:
        """
        Lazily creates and returns the underlying aiohttp session. The session has no total timeout,
        because builds, waits and followed logs can last for a long time. Timeouts are set per request.

        Parameters:
        - None.

        Returns:
        - ClientSession: An open session ready for requests.
        """
        if self._session is None or self._session.closed:
            self._session = ClientSession(
                connector=UnixConnector(path=self.socket_path),
                timeout=ClientTimeout(total=None)
            )

        return self._session

    async def initialize(self) -> None:
        """
        Opens the underlying session and prepares the client for use. Should be called on application startup
        if the client isn't used as an async context manager. Safe to call multiple times.

        Parameters:
        - None.

        Returns:
        - None.
        """
        self._get_session()

    async def close(self) -> None:
        """
        Closes the underlying session and frees its connections.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if self._session is not None and not self._session.closed:
            await self._session.close()

    async def __aenter__(self) -> "UnixSocketClient":
        """
        Enters the async context manager. Ensures the underlying session is created.

        Parameters:
        - None.

        Returns:
        - UnixSocketClient: Self, ready to make requests.
        """
        self._get_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exits the async context manager and closes the session.

        Parameters:
        - exc_type: Exception type, if any.
        - exc_val: Exception value, if any.
        - exc_tb: Exception traceback, if any.

        Returns:
        - None.
        """
        await self.close()

    @staticmethod
    def _prepare_params(
        params: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, str]]:
        """
        Converts query params to the form aiohttp accepts: booleans become "true"/"false", None values are dropped.

        Parameters:
        - params: Query params.

        Returns:
        - Dict: Prepared params or None.
        """
        if not params:
            return None

        prepared = {}

        for key, value in params.items():
            if value is None:
                continue

            if isinstance(value, bool):
                prepared[key] = "true" if value else "false"
            else:
                prepared[key] = str(value)

        return prepared

    async def request(
        self,
        path: str,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ) -> SocketResponse:
        """
        Performs a request and buffers the whole response. HTTP error statuses are not raised, the caller decides.

        Parameters:
        - path: Request path, for example "/containers/json".
        - method: HTTP method.
        - params: Query params.
        - data: Raw body.
        - json: JSON body.
        - headers: Extra headers.
        - timeout: Request timeout in seconds. None means no timeout.

        Returns:
        - SocketResponse: Status, headers and body.

        Raises:
        - SocketError: On connection errors.
        """
        try:
            async with self._get_session().request(
                method=method,
                url=f"{self.base_url}{path}",
                params=self._prepare_params(params),
                data=data,
                json=json,
                headers=headers,
                timeout=ClientTimeout(total=timeout)
            ) as response:
                return SocketResponse(
                    status=response.status,
                    body=await response.read(),
                    headers=dict(response.headers)
                )
        except (ClientError, OSError, TimeoutError) as e:
            raise SocketError(f"{method} {path} failed: {e}") from e

    async def stream(
        self,
        path: str,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ) -> AsyncGenerator[bytes, None]:
        """
        Performs a request and yields the response body in raw chunks as they arrive.

        Parameters:
        - path: Request path.
        - method: HTTP method.
        - params: Query params.
        - data: Raw body.
        - json: JSON body.
        - headers: Extra headers.
        - timeout: Request timeout in seconds. None means no timeout.

        Returns:
        - AsyncGenerator: Raw body chunks.

        Raises:
        - SocketError: On connection errors or an HTTP error status.
        """
        try:
            async with self._get_session().request(
                method=method,
                url=f"{self.base_url}{path}",
                params=self._prepare_params(params),
                data=data,
                json=json,
                headers=headers,
                timeout=ClientTimeout(total=timeout)
            ) as response:
                if response.status >= 400:
                    body = await response.read()

                    raise SocketError(
                        message=body.decode("utf-8", errors="replace"),
                        status=response.status
                    )

                async for chunk in response.content.iter_any():
                    yield chunk
        except (ClientError, OSError, TimeoutError) as e:
            raise SocketError(f"{method} {path} failed: {e}") from e