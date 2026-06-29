"""
Retry with Exponential Backoff (EP-14).
Provides resilience against transient network or database failures.
"""
import asyncio
import logging
from functools import wraps
from typing import Callable, TypeVar, Awaitable

logger = logging.getLogger("Resilience.Retry")
T = TypeVar('T')


def retry_with_backoff(
    max_retries: int = 3, 
    base_delay_sec: float = 1.0, 
    max_delay_sec: float = 10.0,
    exceptions_to_retry: tuple = (Exception,)
):
    """
    Decorator that retries an async function execution with exponential backoff.
    """
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            retries = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except exceptions_to_retry as e:
                    retries += 1
                    if retries > max_retries:
                        logger.error(f"Max retries ({max_retries}) reached for {func.__name__}.")
                        raise e
                    
                    delay = min(base_delay_sec * (2 ** (retries - 1)), max_delay_sec)
                    logger.warning(f"Execution failed for {func.__name__}. Retrying in {delay}s ({retries}/{max_retries}). Error: {str(e)}")
                    await asyncio.sleep(delay)
        return wrapper
    return decorator
