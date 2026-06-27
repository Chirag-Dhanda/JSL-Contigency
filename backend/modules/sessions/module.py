from core.module import BaseModule
from core.di import ServiceContainer
from .service import SessionManager
from logging import getLogger

logger = getLogger("SessionsModule")

class SessionsModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Sessions"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        """Register Session services into the global DI container."""
        logger.debug("Registering Sessions Services...")
        container.register_singleton(SessionManager, SessionManager())

    async def initialize(self) -> None:
        logger.info("Sessions Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Sessions Module Shutdown.")
