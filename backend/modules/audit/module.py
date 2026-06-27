from core.module import BaseModule
from core.di import ServiceContainer
from .service import AuditService
from logging import getLogger

logger = getLogger("AuditModule")

class AuditModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Audit"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        logger.debug("Registering Audit Services...")
        container.register_singleton(AuditService, AuditService())

    async def initialize(self) -> None:
        logger.info("Audit Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Audit Module Shutdown.")
