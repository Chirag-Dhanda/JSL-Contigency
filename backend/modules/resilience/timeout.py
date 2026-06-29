"""
Timeout Abstraction (EP-14).
Enforces SLAs on bounded operations to prevent thread exhaustion.
"""
import asyncio
import logging
from functools import wraps
from typing import Callable, TypeVar, Awaitable

logger = logging.getLogger("Resilience.Timeout")
T = TypeVar('T')


def with_timeout(timeout_sec: float):
    """
    Decorator that cancels an async function if it takes longer than timeout_sec.
    """
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout_sec)
            except asyncio.TimeoutError:
                logger.error(f"Execution of {func.__name__} timed out after {timeout_sec} seconds.")
                raise TimeoutError(f"Operation timed out after {timeout_sec}s")
        return wrapper
    return decorator
