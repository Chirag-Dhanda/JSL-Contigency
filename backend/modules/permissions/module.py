from core.module import BaseModule
from core.di import ServiceContainer
from .service import PermissionEngine
from logging import getLogger

logger = getLogger("PermissionsModule")

class PermissionsModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Permissions"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        """Register Permissions services into the global DI container."""
        logger.debug("Registering Permissions Services...")
        container.register_singleton(PermissionEngine, PermissionEngine())

    async def initialize(self) -> None:
        logger.info("Permissions Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Permissions Module Shutdown.")
