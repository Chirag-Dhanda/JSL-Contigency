import httpx
import logging
import asyncio
from typing import Optional, Dict, Any

from .config import ai_config

logger = logging.getLogger("OllamaConnectionManager")

class ConnectionManager:
    def __init__(self):
        self.base_url = ai_config.ollama_url
        self.timeout = httpx.Timeout(ai_config.timeout_seconds)
        self.client: Optional[httpx.AsyncClient] = None
        self._lock = asyncio.Lock()

    async def get_client(self) -> httpx.AsyncClient:
        async with self._lock:
            if self.client is None or self.client.is_closed:
                self.client = httpx.AsyncClient(timeout=self.timeout)
            return self.client

    async def close(self):
        async with self._lock:
            if self.client and not self.client.is_closed:
                await self.client.aclose()
            self.client = None

    async def request_with_retry(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        url = f"{self.base_url}{endpoint}"
        retries = 0
        
        while retries < ai_config.retry_count:
            try:
                client = await self.get_client()
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except httpx.RequestError as e:
                retries += 1
                logger.warning(f"Ollama connection error: {e}. Retrying {retries}/{ai_config.retry_count}...")
                if retries >= ai_config.retry_count:
                    raise ConnectionError(f"Failed to connect to Ollama at {url} after {ai_config.retry_count} retries.") from e
                await asyncio.sleep(1 * retries) # Exponential backoff
            except httpx.HTTPStatusError as e:
                logger.error(f"Ollama returned HTTP error: {e}")
                raise

connection_manager = ConnectionManager()
