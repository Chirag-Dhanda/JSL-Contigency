"""
Security Hardening Interceptors (EP-14).
Provides Rate Limiting and Data Sanitization for production deployments.
"""
import time
import logging
from typing import Dict
from fastapi import Request, HTTPException

logger = logging.getLogger("Security.Hardening")


class RateLimiter:
    """
    Simple token bucket or window-based rate limiter abstraction.
    In production, this should be backed by Redis via IDistributedCache.
    """
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # Fallback in-memory store for isolated testing: IP -> (count, window_start)
        self._store: Dict[str, Dict[str, float]] = {}

    async def check_rate_limit(self, request: Request) -> None:
        """
        FastAPI dependency to enforce rate limits per client IP.
        Raises HTTP 429 Too Many Requests if threshold is breached.
        """
        # Note: In a real deployment behind a load balancer, use X-Forwarded-For
        client_ip = request.client.host if request.client else "unknown"
        
        current_time = time.time()
        record = self._store.get(client_ip)
        
        if not record or (current_time - record["window_start"]) > self.window_seconds:
            # Reset window
            self._store[client_ip] = {"count": 1, "window_start": current_time}
            return
            
        if record["count"] >= self.max_requests:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(status_code=429, detail="Too Many Requests. Please try again later.")
            
        record["count"] += 1


def sanitize_output(data: dict) -> dict:
    """
    Ensures sensitive fields (like password hashes or internal keys) 
    never leak via API responses.
    """
    sensitive_keys = {"password", "hash", "secret", "token", "ssn"}
    sanitized = {}
    
    for k, v in data.items():
        if any(sk in k.lower() for sk in sensitive_keys):
            sanitized[k] = "[REDACTED]"
        elif isinstance(v, dict):
            sanitized[k] = sanitize_output(v)
        else:
            sanitized[k] = v
            
    return sanitized
