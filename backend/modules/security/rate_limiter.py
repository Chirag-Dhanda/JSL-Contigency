from collections import defaultdict
from datetime import datetime, timezone, timedelta
from typing import Dict, List
from logging import getLogger
from exceptions.base import BaseApplicationException

logger = getLogger("RateLimiter")

class RateLimitExceeded(BaseApplicationException):
    def __init__(self, message="Too Many Requests"):
        super().__init__(message=message, status_code=429, error_code="RATE_LIMIT_EXCEEDED", title="Rate Limit Exceeded")

class RateLimiter:
    """In-memory sliding window rate limiter for testing/functional verification."""
    
    def __init__(self):
        # Maps IP to a list of timestamps
        self._history: Dict[str, List[datetime]] = defaultdict(list)
        self.MAX_REQUESTS = 5
        self.WINDOW_SECONDS = 10
        
    async def check_rate_limit(self, client_ip: str) -> None:
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(seconds=self.WINDOW_SECONDS)
        
        # Clean old requests
        self._history[client_ip] = [t for t in self._history[client_ip] if t > window_start]
        
        if len(self._history[client_ip]) >= self.MAX_REQUESTS:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise RateLimitExceeded()
            
        self._history[client_ip].append(now)
