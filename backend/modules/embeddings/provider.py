import logging
import httpx
import asyncio
from typing import List, Optional
from modules.ai.config import ai_config

logger = logging.getLogger("OllamaEmbeddingProvider")

class OllamaEmbeddingProvider:
    """Handles communication with the Ollama Embedding API."""
    
    def __init__(self):
        self.base_url = ai_config.ollama_url
        self.model = ai_config.embedding_model
        
    async def check_health(self) -> bool:
        """Verifies Ollama is reachable."""
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama Health Check Failed: {e}")
            return False

    async def get_embedding(self, text: str, retry_count: int = 3) -> Optional[List[float]]:
        """Requests an embedding vector with exponential backoff retry."""
        payload = {
            "model": self.model,
            "prompt": text
        }
        
        for attempt in range(retry_count):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(f"{self.base_url}/api/embeddings", json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        return data.get("embedding", [])
                    else:
                        logger.warning(f"Ollama returned {response.status_code}")
            except Exception as e:
                logger.warning(f"Embedding request failed on attempt {attempt+1}: {e}")
                
            await asyncio.sleep(2 ** attempt) # Exponential backoff
            
        logger.error(f"Failed to get embedding after {retry_count} attempts.")
        return None

embedding_provider = OllamaEmbeddingProvider()
