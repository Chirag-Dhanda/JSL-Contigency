from core.module import BaseModule
from core.di import ServiceContainer
import logging
from typing import Dict, Callable

from .provider import embedding_provider
from .engine import embedding_engine

logger = logging.getLogger("EmbeddingsModule")

class EmbeddingsModule(BaseModule):
    """
    Enterprise Embeddings Module.
    Responsible for initializing the embedding engine, managing Ollama provider connections,
    and handling the background embedding queue.
    """
    
    @property
    def name(self) -> str:
        return "Embeddings"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        pass
        
    async def initialize(self) -> None:
        """Initialize Embedding Engine and background workers."""
        try:
            logger.info("Initializing Embeddings Module...")
            
            # Start background workers for processing queue
            await embedding_engine.start_workers()
            
            logger.info("Embeddings Module initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Embeddings Module: {e}")
            raise
            
    async def shutdown(self) -> None:
        """Gracefully shutdown background workers."""
        logger.info("Shutting down Embeddings Module...")
        await embedding_engine.stop_workers()

    def register_health_checks(self) -> Dict[str, Callable[[], bool]]:
        """Return health checks for the Embeddings module."""
        async def check_provider_health():
            return await embedding_provider.check_health()
            
        return {
            "embedding_provider": lambda: True # Ideally wrapping the async call or polling a cached status
        }
