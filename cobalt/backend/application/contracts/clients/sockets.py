#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Literal, AsyncGenerator

from application.clients.sockets.shared import SocketResponse


class AbstractSocketClient(ABC):
    """
    Abstract HTTP-over-socket client.
    """

    @abstractmethod
    async def close(self) -> None:
        """
        Closes the underlying session and frees its connections.

        Parameters:
        - None.

        Returns:
        - None.
        """
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> "AbstractSocketClient":
        """
        Enters the async context manager.

        Parameters:
        - None.

        Returns:
        - AbstractSocketClient: Self, ready to make requests.
        """
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
    def stream(
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
        raise NotImplementedError