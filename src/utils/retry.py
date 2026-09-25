"""Exponential backoff retry decorator for LLM API calls."""
import time
import functools
from typing import Callable, Tuple, Type
from src.utils.logger import logger


def retry_with_backoff(
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    retry_exceptions: Tuple[Type[Exception], ...] = (Exception,),
    initial_wait: float = 1.0,
):
    """Decorator that retries a function with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts.
        backoff_factor: Multiplier for wait time between retries.
        retry_exceptions: Exception types that trigger a retry.
        initial_wait: Initial wait time in seconds.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = initial_wait
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retry_exceptions as e:
                    if attempt == max_retries:
                        logger.error(f"[retry] {func.__name__} failed after {max_retries} retries: {e}")
                        raise
                    logger.warning(
                        f"[retry] {func.__name__} attempt {attempt + 1}/{max_retries} failed: {e}. "
                        f"Retrying in {wait:.1f}s..."
                    )
                    time.sleep(wait)
                    wait *= backoff_factor
        return wrapper
    return decorator
