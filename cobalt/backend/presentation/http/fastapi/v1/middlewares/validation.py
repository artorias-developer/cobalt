#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from application.contracts.loggers import AbstractLogger


class HttpValidationMiddleware:
    """
    Handles Pydantic validation errors and returns the first human-readable error message.
    """
    logger: AbstractLogger

    def __init__(
        self,
        logger: AbstractLogger
    ):
        self.logger = logger

    @staticmethod
    def get_validation_message(exc: RequestValidationError) -> str:
        """
        Extracts a human-readable message from the first validation error.

        Parameters:
        - exc: RequestValidationError exception.

        Returns:
        - str: Human-readable error message.
        """
        error = exc.errors()[0]

        field = error.get("loc", [])
        field_name = str(field[-1]).replace("_", " ").title() if field else "Unknown"
        error_type = error.get("type", "")
        ctx = error.get("ctx", {})
        msg = error.get("msg", "")

        match error_type:
            case "missing":
                return f"{field_name} is required"

            case "string_too_short":
                min_length = ctx.get("min_length", "?")
                return f"{field_name} must be at least {min_length} characters long"

            case "string_too_long":
                max_length = ctx.get("max_length", "?")
                return f"{field_name} cannot be longer than {max_length} characters"

            case "string_pattern_mismatch":
                return f"{field_name} contains invalid characters"

            case "greater_than":
                gt = ctx.get("gt", "?")
                return f"{field_name} must be greater than {gt}"

            case "greater_than_equal":
                ge = ctx.get("ge", "?")
                return f"{field_name} must be greater than or equal to {ge}"

            case "less_than":
                lt = ctx.get("lt", "?")
                return f"{field_name} must be less than {lt}"

            case "less_than_equal":
                le = ctx.get("le", "?")
                return f"{field_name} must be less than or equal to {le}"

            case "int_parsing":
                return f"{field_name} must be a valid integer"

            case "float_parsing":
                return f"{field_name} must be a valid number"

            case "bool_parsing":
                return f"{field_name} must be a valid boolean"

            case "enum":
                expected = ctx.get("expected", "?")
                return f"{field_name} must be one of the allowed values: {expected}"

            case "list_type":
                return f"{field_name} must be a list"

            case "too_short":
                min_length = ctx.get("min_length", "?")
                return f"{field_name} must contain at least {min_length} item(s)"

            case "too_long":
                max_length = ctx.get("max_length", "?")
                return f"{field_name} cannot contain more than {max_length} item(s)"

            case "value_error":
                return f"{field_name}: {msg}"

            case _:
                return f"{field_name} failed validation"

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