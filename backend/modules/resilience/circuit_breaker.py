"""
Circuit Breaker Pattern (EP-14).
Prevents cascading failures when external dependencies (DB, AI, Connectors) degrade.
"""
import time
import logging
from enum import Enum
from typing import Callable, Any, TypeVar, Awaitable
from functools import wraps

logger = logging.getLogger("Resilience.CircuitBreaker")

class CircuitState(Enum):
    CLOSED = "CLOSED"       # Normal operation, traffic flows
    OPEN = "OPEN"           # Failing, traffic blocked
    HALF_OPEN = "HALF_OPEN" # Testing recovery, limited traffic flows

T = TypeVar('T')


class CircuitBreakerOpenException(Exception):
    pass


class CircuitBreaker:
    def __init__(
        self, 
        name: str, 
        failure_threshold: int = 5, 
        recovery_timeout_sec: float = 30.0
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        logger.warning(f"Circuit '{self.name}' recorded failure ({self.failure_count}/{self.failure_threshold})")
        
        if self.failure_count >= self.failure_threshold and self.state == CircuitState.CLOSED:
            self._open_circuit()

    def record_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self._close_circuit()
        self.failure_count = 0

    def _open_circuit(self):
        self.state = CircuitState.OPEN
        logger.error(f"Circuit '{self.name}' is OPEN. Traffic blocked for {self.recovery_timeout_sec}s.")

    def _close_circuit(self):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        logger.info(f"Circuit '{self.name}' is CLOSED. Normal operation resumed.")

    def can_execute(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
            
        if self.state == CircuitState.OPEN:
            if (time.time() - self.last_failure_time) > self.recovery_timeout_sec:
                self.state = CircuitState.HALF_OPEN
                logger.info(f"Circuit '{self.name}' transitioning to HALF-OPEN. Testing recovery.")
                return True
            return False
            
        return True # HALF-OPEN


def with_circuit_breaker(breaker: CircuitBreaker):
    """Decorator to wrap async functions in a circuit breaker."""
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            if not breaker.can_execute():
                raise CircuitBreakerOpenException(f"Circuit {breaker.name} is OPEN.")
                
            try:
                result = await func(*args, **kwargs)
                breaker.record_success()
                return result
            except Exception as e:
                breaker.record_failure()
                raise e
        return wrapper
    return decorator
