#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

import logging
from sys import stdout
from logging.handlers import RotatingFileHandler
from typing import List

from structlog import (
    configure,
    get_logger
)
from structlog.stdlib import (
    add_log_level,
    add_logger_name,
    PositionalArgumentsFormatter,
    ExtraAdder,
    ProcessorFormatter,
    LoggerFactory,
    BoundLogger
)
from structlog.processors import (
    StackInfoRenderer,
    TimeStamper,
    ExceptionRenderer
)
from structlog.types import (
    Processor,
    EventDict
)
from structlog.contextvars import merge_contextvars

from application.contracts.loggers import AbstractLogger
from infrastructure.configs import ApplicationConfig
from infrastructure.loggers import StructlogLogger


def drop_color_message_key(
    logger: object,
    method: str,
    event_dict: EventDict
) -> EventDict:
    """
    Drops the color_message key from the event dict added by uvicorn.

    Parameters:
    - logger: Logger instance.
    - method: Log method name.
    - event_dict: Structlog event dictionary.

    Returns:
    - EventDict: Event dictionary without color_message key.
    """
    event_dict.pop("color_message", None)
    return event_dict

def structlog_render_message(
    logger: object,
    method: str,
    event_dict: EventDict
) -> str:
    """
    Renders the event dict as a plain string matching the configured log format.

    Parameters:
    - logger: Logger instance.
    - method: Log method name.
    - event_dict: Structlog event dictionary.

    Returns:
    - str: Formatted log string with newlines escaped.
    """
    timestamp = event_dict.get("timestamp", "")
    level = event_dict.get("level", "").upper()
    message = event_dict.get("event", "")
    exception = event_dict.get("exception", "")

    if exception:
        return f"{timestamp} {level} {message}\n{exception}"

    return f"{timestamp} {level} {message}"

def create_structlog_logger(
    config: ApplicationConfig
) -> AbstractLogger:
    """
    Creates a Structlog logger.

    Parameters:
    - config: ApplicationConfig object.

    Returns:
    - AbstractLogger: AbstractLogger object.
    """
    config.logging.log_dir.mkdir(exist_ok=True)

    shared_processors: List[Processor] = [
        merge_contextvars,
        add_logger_name,
        add_log_level,
        PositionalArgumentsFormatter(),
        ExtraAdder(),
        drop_color_message_key,
        TimeStamper(fmt=config.logging.date_fmt, utc=True),
        StackInfoRenderer(),
        ExceptionRenderer(),
    ]

    configure(
        processors=shared_processors + [
            ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=LoggerFactory(),
        wrapper_class=BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            ProcessorFormatter.remove_processors_meta,
            structlog_render_message,
        ],
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()

    console_handler = logging.StreamHandler(stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        filename=str(config.logging.log_dir / config.logging.log_file),
        maxBytes=config.logging.max_size,
        backupCount=config.logging.backup_count
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    log_config = {
        "uvicorn": {
            "clear_handlers": True,
            "propagate": True,
        },
        "uvicorn.error": {
            "level": logging.WARNING,
            "clear_handlers": True,
            "propagate": True,
        },
        "uvicorn.access": {
            "level": logging.WARNING,
            "clear_handlers": True,
            "propagate": True,
        },
        "apscheduler": {
            "level": logging.WARNING,
            "propagate": True,
        },
        "httpx": {
            "level": logging.WARNING,
            "propagate": True,
        },
        "httpcore": {
            "level": logging.WARNING,
            "propagate": True,
        },
        "aiohttp": {
            "level": logging.WARNING,
            "propagate": True,
        },
        "sqlalchemy": {
            "level": logging.WARNING,
            "propagate": config.database.echo,
        },
        "sqlalchemy.engine": {
            "level": logging.WARNING,
            "propagate": config.database.echo,
        },
        "sqlalchemy.pool": {
            "level": logging.WARNING,
            "propagate": config.database.echo,
        }
    }

    for name, params in log_config.items():
        logger = logging.getLogger(name)

        if params.get("clear_handlers"):
            logger.handlers.clear()

        if "level" in params:
            logger.setLevel(params["level"])

        if "propagate" in params:
            logger.propagate = params["propagate"]

    return StructlogLogger(
        logger=get_logger(config.logging.logger_name)
    )