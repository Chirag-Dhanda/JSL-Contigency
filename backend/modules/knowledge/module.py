from core.module import BaseModule
from core.di import ServiceContainer
from .service import KnowledgeService
from logging import getLogger

logger = getLogger("KnowledgeModule")

class KnowledgeModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Knowledge"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        logger.debug("Registering Knowledge Engine Service...")
        self.svc = KnowledgeService()
        container.register_singleton(KnowledgeService, self.svc)

    async def initialize(self) -> None:
        logger.info("Enterprise Knowledge Engine Initialized.")

    async def shutdown(self) -> None:
        logger.info("Enterprise Knowledge Engine Shutdown.")
