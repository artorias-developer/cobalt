#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from asyncio import Task, Queue, Semaphore, create_task
from typing import Any, Callable

from application.contracts.queues import AbstractQueue
from application.contracts.loggers import AbstractLogger


class AsyncioQueue(AbstractQueue):
    """
    Async in-process queue using asyncio.Queue with a semaphore-limited worker pool.
    """
    _queue: Queue
    _semaphore: Semaphore
    _workers: list[Task]

    logger: AbstractLogger
    max_workers: int

    def __init__(
        self,
        logger: AbstractLogger,
        max_workers: int = 5
    ):
        self.logger = logger
        self.max_workers = max_workers

    async def initialize(self) -> None:
        """
        Initializes the queue, semaphore, and worker pool.

        Parameters:
        - None.

        Returns:
        - None.
        """
        self._queue = Queue()
        self._semaphore = Semaphore(self.max_workers)
        self._workers = [
            create_task(self._worker())
            for _ in range(self.max_workers)
        ]

    async def _worker(self) -> None:
        """
        Worker coroutine that continuously pulls tasks from the queue and executes them.

        Parameters:
        - None.

        Returns:
        - None.
        """
        while True:
            function, args, kwargs = await self._queue.get()

            async with self._semaphore:
                await self._execute_with_error_handling(function, *args, **kwargs)

            self._queue.task_done()

    async def _execute_with_error_handling(
        self,
        function: Callable,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Wrapper that handles errors in task execution.

        Parameters:
        - function: Function to execute.
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        try:
            await function(*args, **kwargs)
        except Exception:
            self.logger.exception(f'Error while executing task "{function.__name__}":')

    async def enqueue(
        self,
        function: Callable,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Adds a task to the queue for asynchronous execution.
        Queue size is unlimited. Tasks are processed concurrently up to max_workers.

        Parameters:
        - function: Async function to execute.
        - *args: Positional arguments for the function.
        - **kwargs: Keyword arguments for the function.

        Returns:
        - None.
        """
        if not hasattr(self, "_queue"):
            await self.initialize()

        await self._queue.put((function, args, kwargs))