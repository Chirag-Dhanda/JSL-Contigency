import logging
import time
import hashlib
from typing import Dict, Any, Optional

logger = logging.getLogger("IntelligentCache")

class IntelligentCache:
    """In-memory KV store to bypass LLM processing for repeated questions."""
    
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def _hash_query(self, query: str) -> str:
        return hashlib.md5(query.lower().strip().encode('utf-8')).hexdigest()

    def get_cached_response(self, query: str) -> Optional[str]:
        query_hash = self._hash_query(query)
        cached_item = self._store.get(query_hash)
        
        if cached_item:
            if time.time() > cached_item["expires_at"]:
                logger.debug(f"Cache expired for {query_hash}")
                del self._store[query_hash]
                return None
            logger.info(f"Cache Hit for query: '{query}'")
            return cached_item["response"]
            
        return None

    def cache_response(self, query: str, response: str, ttl_seconds: int = 3600):
        query_hash = self._hash_query(query)
        self._store[query_hash] = {
            "response": response,
            "expires_at": time.time() + ttl_seconds
        }
        logger.debug(f"Cached response for {query_hash} with TTL {ttl_seconds}s")
