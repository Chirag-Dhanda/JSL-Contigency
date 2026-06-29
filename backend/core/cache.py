"""
Distributed Cache Abstraction (EP-14).
Prepares EKOS for horizontal scaling by abstracting caching logic
so it can be backed by Redis or Memcached in future deployments.
"""
import time
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict

class IDistributedCache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass

    @abstractmethod
    async def clear(self) -> None:
        pass


class InMemoryDistributedCacheMock(IDistributedCache):
    """
    In-memory mock proving the caching architecture.
    To be replaced by RedisDistributedCache in production.
    """
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    async def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if not entry:
            return None
            
        if time.time() > entry["expires_at"]:
            del self._store[key]
            return None
            
        return entry["value"]

    async def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        self._store[key] = {
            "value": value,
            "expires_at": time.time() + ttl_seconds
        }

    async def delete(self, key: str) -> None:
        self._store.pop(key, None)

    async def clear(self) -> None:
        self._store.clear()
