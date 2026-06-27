from core.module import BaseModule
from core.di import ServiceContainer
from .service import RoadmapService
from logging import getLogger

logger = getLogger("RoadmapModule")

class RoadmapModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Roadmap"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        logger.debug("Registering Roadmap Service...")
        container.register_singleton(RoadmapService, RoadmapService())

    async def initialize(self) -> None:
        logger.info("Roadmap Engine Initialized.")

    async def shutdown(self) -> None:
        logger.info("Roadmap Engine Shutdown.")
