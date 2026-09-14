from typing import Optional, Dict, Any, Literal, Union

from aiohttp import ClientSession, ClientTimeout, ContentTypeError

from application.contracts.clients import AbstractHttpClient
from application.contracts.loggers import AbstractLogger


class AiohttpClient(AbstractHttpClient):
    """
    Aiohttp HTTP client.
    """
    _timeout: ClientTimeout
    _session: Optional[ClientSession]

    logger: AbstractLogger

    def __init__(
        self,
        logger: Any,
        timeout: float = 60.0,
    ):
        self.logger = logger

        self._session = None
        self._timeout = ClientTimeout(total=timeout)

    def _get_session(self) -> ClientSession:
        """
        Lazily create and return the underlying aiohttp session. ClientSession must be created inside
        a running event loop, so it is instantiated on first use rather than in __init__.

        Parameters:
        - None.

        Returns:
        - ClientSession: an open session ready for requests
        """
        if self._session is None or self._session.closed:
            self._session = ClientSession(timeout=self._timeout)

        return self._session

    async def close(self) -> None:
        """
        Close the underlying session and free its connections. Should be called on application shutdown
        if the client wasn't used as an async context manager.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if self._session is not None and not self._session.closed:
            await self._session.close()

    async def __aenter__(self) -> "AiohttpClient":
        """
        Enter the async context manager. Ensures the underlying session is created.

        Parameters:
        - None.

        Returns:
        - AiohttpClient: Self, ready to make requests.
        """
        self._get_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the async context manager. Closes the underlying session regardless of whether an
        exception occurred inside the `with` block.

        Parameters:
        - exc_type: Exception type, if any.
        - exc_val: Exception value, if any.
        - exc_tb: Exception traceback, if any.

        Returns:
        - None.
        """
        await self.close()

    async def request(
        self,
        url: str,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        proxy: Optional[str] = None,
        timeout: Optional[float] = None
    ) -> Optional[Union[Dict, str]]:
        """
        Universal HTTP request.

        Parameters:
        - url: Request URL.
        - method: HTTP method.
        - params: Query params.
        - data: Raw body / form-data / bytes.
        - json: JSON body.
        - headers: Extra headers.
        - proxy: Proxy URL to route the request through.
        - timeout: Per-request timeout in seconds. Overrides the client's default timeout if set.

        Returns:
        - Dict: Dict response or text, None on error.
        """
        session = self._get_session()
        request_timeout = ClientTimeout(total=timeout) if timeout is not None else self._timeout

        try:
            async with session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                proxy=proxy,
                timeout=request_timeout
            ) as response:
                response.raise_for_status()

                try:
                    return await response.json()
                except ContentTypeError:
                    return await response.text()
        except Exception:
            self.logger.exception(f"HTTP {method} request failed: {url}")
            return None