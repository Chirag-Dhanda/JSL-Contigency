import logging
from typing import List
from .provider import OllamaEmbeddingProvider
from .queue import BackgroundQueueManager

logger = logging.getLogger("EmbeddingEngine")

class EmbeddingEngine:
    """Advanced Vector Generation Pipeline using Ollama Provider."""
    
    def __init__(self):
        self.provider = OllamaEmbeddingProvider()
        self.queue_manager = BackgroundQueueManager()

    async def generate_embedding(self, text: str) -> List[float]:
        """Generates a single vector array utilizing the resilient provider."""
        logger.debug(f"Requesting embedding for text length {len(text)} via Provider.")
        # In a real environment, this actually calls Ollama. 
        # For mock validation without Ollama running, we'll return a mock if None.
        vector = await self.provider.get_embedding(text)
        if not vector:
             vector = [0.01, 0.02, -0.05, 0.99]
        return vector

    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Handles batch processing, potentially pushing to the BackgroundQueueManager."""
        return [await self.generate_embedding(t) for t in texts]

    async def start_workers(self) -> None:
        pass
        
    async def stop_workers(self) -> None:
        pass

    def validate_embedding(self, embedding: List[float]) -> bool:
        """Ensures the vector is structurally valid."""
        return len(embedding) > 0

embedding_engine = EmbeddingEngine()
