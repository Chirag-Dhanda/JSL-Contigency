from core.module import BaseModule
from core.di import ServiceContainer
import logging
from typing import Dict, Callable

from .manager import index_manager

logger = logging.getLogger("IndexManagementModule")

class IndexManagementModule(BaseModule):
    """
    Enterprise Index Management Module.
    Responsible for orchestrating vector database indexes and providing administrative APIs.
    """
    
    @property
    def name(self) -> str:
        return "IndexManagement"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        pass
        
    async def initialize(self) -> None:
        """Initialize Index Management Module."""
        logger.info("Initializing Index Management Module...")
            
    async def shutdown(self) -> None:
        """Gracefully shutdown Index Management Module."""
        logger.info("Shutting down Index Management Module...")

    def register_health_checks(self) -> Dict[str, Callable[[], bool]]:
        """Return health checks for the Index Management module."""
        return {
            "index_manager": lambda: True
        }
