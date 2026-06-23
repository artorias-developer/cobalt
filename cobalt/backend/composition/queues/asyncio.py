#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.loggers import AbstractLogger
from application.contracts.queues import AbstractQueue
from infrastructure.queues import AsyncioQueue


def create_asyncio_queue(
    logger: AbstractLogger
) -> AbstractQueue:
    """
    Creates the Asyncio queue.

    Parameters:
    - logger: AbstractLogger object.

    Returns:
    - AbstractQueue: AbstractQueue object.
    """
    return AsyncioQueue(
        max_workers=2,
        logger=logger
    )
