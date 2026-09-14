from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Literal, Union


class AbstractHttpClient(ABC):
    """
    Abstract HTTP client.
    """

    @abstractmethod
    async def close(self) -> None:
        """
        Close the underlying session and free its connections. Should be called on application shutdown
        if the client wasn't used as an async context manager.

        Parameters:
        - None.

        Returns:
        - None.
        """
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> "AbstractHttpClient":
        """
        Enter the async context manager. Ensures the underlying session is created.

        Parameters:
        - None.

        Returns:
        - AbstractHttpClient: Self, ready to make requests.
        """
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError