from core.module import BaseModule
from core.di import ServiceContainer
from .service import LearningService
from logging import getLogger

logger = getLogger("LearningModule")

class LearningModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Learning"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        logger.debug("Registering Learning Service...")
        container.register_singleton(LearningService, LearningService())

    async def initialize(self) -> None:
        logger.info("Learning Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Learning Module Shutdown.")
