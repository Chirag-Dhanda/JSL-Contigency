import logging
import time

logger = logging.getLogger("CircuitBreaker")

class CircuitBreaker:
    """Protects the system from cascaded failures."""
    
    def __init__(self, failure_threshold: int = 3, reset_timeout_seconds: int = 60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout_seconds
        
        self.failures = 0
        self.is_open = False
        self.last_failure_time = 0

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            logger.error("CIRCUIT BREAKER TRIPPED! Failing fast on subsequent requests.")
            self.is_open = True

    def check_status(self) -> bool:
        """Returns True if safe to proceed, False if circuit is Open."""
        if self.is_open:
            if time.time() - self.last_failure_time > self.reset_timeout:
                logger.info("Circuit Breaker reset timeout reached. Half-opening circuit.")
                self.is_open = False
                self.failures = 0
                return True
            return False
        return True
