from core.module import BaseModule
from core.di import ServiceContainer
import logging
from typing import Dict, Callable

from .client import db_client
from .collections import collection_manager
from .health import health_service

logger = logging.getLogger("VectorDBModule")

class VectorDBModule(BaseModule):
    """
    Enterprise Vector Database Module.
    Responsible for initializing ChromaDB, registering enterprise collections,
    and exposing health checks.
    """
    
    @property
    def name(self) -> str:
        return "VectorDB"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        """Register VectorDB services into the IoC container."""
        # Future: container.register_singleton("vector_db_client", db_client)
        pass
        
    async def initialize(self) -> None:
        """Initialize ChromaDB and prepare collections."""
        try:
            logger.info("Initializing VectorDB Module...")
            
            # 1. Initialize DB Client (Storage + Connection)
            db_client.initialize()
            
            # 2. Register standard enterprise collections
            collection_manager.register_collections()
            
            logger.info("VectorDB Module initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize VectorDB Module: {e}")
            raise
            
    async def shutdown(self) -> None:
        """Gracefully shutdown VectorDB connections."""
        logger.info("Shutting down VectorDB Module...")
        # ChromaDB Python client handles its own shutdown logic typically,
        # but if using HttpClient, we might need to close connections in the future.
        pass

    def register_health_checks(self) -> Dict[str, Callable[[], bool]]:
        """Return health checks for the VectorDB module."""
        def check_vector_db_health():
            status = health_service.check_health()
            return status["status"] == "healthy"
            
        return {
            "vector_db": check_vector_db_health
        }
