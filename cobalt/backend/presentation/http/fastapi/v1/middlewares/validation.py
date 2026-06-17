#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from application.contracts.loggers import AbstractLogger
from application.contracts.managers import AbstractI18nManager


class HttpValidationMiddleware:
    """
    Handles Pydantic validation errors and returns the first human-readable error message.
    """
    i18n_manager: AbstractI18nManager
    logger: AbstractLogger

    _: Callable

    def __init__(
        self,
        i18n_manager: AbstractI18nManager,
        logger: AbstractLogger
    ):
        self.logger = logger
        self.i18n_manager = i18n_manager

        self._ = i18n_manager.gettext

    def get_validation_message(
        self,
        exc: RequestValidationError
    ) -> str:
        """
        Extracts a human-readable message from the first validation error.

        Parameters:
        - exc: RequestValidationError exception.

        Returns:
        - str: Human-readable error message.
        """
        error = exc.errors()[0]

        field = error.get("loc", [])
        field_name = self._(str(field[-1]).replace("_", " ").capitalize()) if field else self._("Unknown")
        error_type = error.get("type", "")
        ctx = error.get("ctx", {})
        msg = error.get("msg", "")

        match error_type:
            case "missing":
                return self._("{field_name} is required").format(
                    field_name=field_name
                )

            case "string_too_short":
                min_length = ctx.get("min_length", "?")
                return self._("{field_name} must be at least {min_length} characters long").format(
                    field_name=field_name,
                    min_length=min_length
                )

            case "string_too_long":
                max_length = ctx.get("max_length", "?")
                return self._("{field_name} cannot be longer than {max_length} characters").format(
                    field_name=field_name,
                    max_length=max_length
                )

            case "string_pattern_mismatch":
                return self._("{field_name} contains invalid characters").format(
                    field_name=field_name
                )

            case "greater_than":
                gt = ctx.get("gt", "?")
                return self._("{field_name} must be greater than {gt}").format(
                    field_name=field_name,
                    gt=gt
                )

            case "greater_than_equal":
                ge = ctx.get("ge", "?")
                return self._("{field_name} must be greater than or equal to {ge}").format(
                    field_name=field_name,
                    ge=ge
                )

            case "less_than":
                lt = ctx.get("lt", "?")
                return self._("{field_name} must be less than {lt}").format(
                    field_name=field_name,
                    lt=lt
                )

            case "less_than_equal":
                le = ctx.get("le", "?")
                return self._("{field_name} must be less than or equal to {le}").format(
                    field_name=field_name,
                    le=le
                )

            case "int_parsing":
                return self._("{field_name} must be a valid integer").format(
                    field_name=field_name
                )

            case "float_parsing":
                return self._("{field_name} must be a valid number").format(
                    field_name=field_name
                )

            case "bool_parsing":
                return self._("{field_name} must be a valid boolean").format(
                    field_name=field_name
                )

            case "enum":
                expected = ctx.get("expected", "?")
                return self._("{field_name} must be one of the allowed values: {expected}").format(
                    field_name=field_name,
                    expected=expected
                )

            case "list_type":
                return self._("{field_name} must be a list").format(
                    field_name=field_name
                )

            case "too_short":
                min_length = ctx.get("min_length", "?")
                return self._("{field_name} must contain at least {min_length} item(s)").format(
                    field_name=field_name,
                    min_length=min_length
                )

            case "too_long":
                max_length = ctx.get("max_length", "?")
                return self._("{field_name} cannot contain more than {max_length} item(s)").format(
                    field_name=field_name,
                    max_length=max_length
                )

            case "value_error":
                return self._("{field_name}: {msg}").format(
                    field_name=field_name,
                    msg=msg
                )

            case _:
                return self._("{field_name} failed validation").format(
                    field_name=field_name
                )

    async def dispatch(
        self,
        request: Request,
        exc: RequestValidationError
    ) -> Response:
        """
        Dispatches Pydantic validation errors and returns the first human-readable error message.

        Parameters:
        - request: Request object.
        - exc: RequestValidationError exception.

        Returns:
        - JSONResponse: JSON response with the first field-level error message.
        """
        message = self.get_validation_message(exc=exc)

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": message
            }
        )