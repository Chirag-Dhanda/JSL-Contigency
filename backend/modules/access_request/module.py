from core.module import BaseModule
from core.di import ServiceContainer
from .service import AccessRequestService
from logging import getLogger

logger = getLogger("AccessRequestModule")

class AccessRequestModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "AccessRequest"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        logger.debug("Registering Access Request Services...")
        container.register_singleton(AccessRequestService, AccessRequestService())

    async def initialize(self) -> None:
        logger.info("Access Request Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Access Request Module Shutdown.")
