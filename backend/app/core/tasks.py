"""
Background task system for running simulations.
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Callable

logger = logging.getLogger("flow.tasks")


class TaskQueue:
    """Simple in-memory task queue for simulation execution."""

    def __init__(self, max_concurrent: int = 4):
        self.max_concurrent = max_concurrent
        self._running = 0
        self._queue: list[Callable] = []
        self._tasks: dict[str, asyncio.Task] = {}

    async def submit(self, task_id: str, coro: Callable):
        """Submit a coroutine for execution."""
        if self._running >= self.max_concurrent:
            self._queue.append(lambda: self._execute(task_id, coro))
            logger.info(f"Task {task_id} queued (queue size: {len(self._queue)})")
        else:
            await self._execute(task_id, coro)

    async def _execute(self, task_id: str, coro: Callable):
        """Execute a task."""
        self._running += 1
        logger.info(f"Task {task_id} started (active: {self._running})")

        try:
            task = asyncio.create_task(coro())
            self._tasks[task_id] = task
            await task
            logger.info(f"Task {task_id} completed")
        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")
        finally:
            self._running -= 1
            del self._tasks[task_id]

            # Process queue
            if self._queue and self._running < self.max_concurrent:
                next_task = self._queue.pop(0)
                await next_task()

    def cancel(self, task_id: str) -> bool:
        """Cancel a running task."""
        if task_id in self._tasks:
            self._tasks[task_id].cancel()
            return True
        return False

    @property
    def active_count(self) -> int:
        return self._running

    @property
    def queue_size(self) -> int:
        return len(self._queue)


# Global task queue
task_queue = TaskQueue(max_concurrent=4)
