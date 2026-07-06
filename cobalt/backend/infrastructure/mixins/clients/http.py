#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional, Dict, Any, Literal, Union

from httpx import AsyncClient

from application.contracts.loggers import AbstractLogger


class HttpClientMixin:
    """
    Mixin for HTTP client.
    """
    _client: AsyncClient

    logger: AbstractLogger

    def __init__(
        self,
        logger: Any,
        timeout: float = 60.0
    ):
        self.logger = logger

        self._client = AsyncClient(timeout=timeout)

    async def request(
        self,
        url: str,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Optional[Union[Dict, str]]:
        """
        Universal HTTP request.

        Parameters:
        - path: URL path
        - method: HTTP method
        - params: query params
        - data: raw body / form-data / bytes
        - json: JSON body
        - headers: extra headers

        Returns:
        - Dict: Dict response or text, None on error.
        """
        try:
            response = await self._client.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json,
                headers=headers,
            )
            response.raise_for_status()
        except Exception:
            self.logger.exception(f"HTTP {method} request failed: {url}")
            return None

        try:
            return response.json()
        except Exception:
            return response.text
