from core.module import BaseModule
from core.di import ServiceContainer
from .engine import TemplateEngine
from logging import getLogger

logger = getLogger("TemplatesModule")

class TemplatesModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Templates"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        logger.debug("Registering TemplateEngine as Singleton...")
        container.register_singleton(TemplateEngine, TemplateEngine())

    async def initialize(self) -> None:
        logger.info("Templates Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Templates Module Shutdown.")
