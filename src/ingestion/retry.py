"""
lecture 9: Retry Strategy-ის საკუთარი, გამჭვირვალე იმპლემენტაცია (exponential backoff).
"""

import functools
import logging
import time
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def retry_with_backoff(
    exceptions: tuple,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 8.0,
):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            attempt = 1
            delay = base_delay
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt >= max_attempts:
                        logger.error("ცდა #%d ჩავარდა საბოლოოდ: %s", attempt, exc)
                        raise
                    logger.warning("ცდა #%d ჩავარდა (%s), თავიდან %.1fწმ-ში...", attempt, exc, delay)
                    time.sleep(delay)
                    delay = min(delay * 2, max_delay)
                    attempt += 1
        return wrapper
    return decorator
