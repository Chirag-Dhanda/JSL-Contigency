from core.module import BaseModule
from core.di import ServiceContainer
from .service import AuthorizationPipeline
from modules.permissions.service import PermissionEngine
from logging import getLogger

logger = getLogger("AuthorizationModule")

class AuthorizationModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Authorization"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        """Register Authorization services into the global DI container."""
        logger.debug("Registering Authorization Services...")
        
        # Resolve the PermissionEngine which should have been registered by PermissionsModule
        permission_engine = container.resolve(PermissionEngine)
        container.register_singleton(AuthorizationPipeline, AuthorizationPipeline(permission_engine))

    async def initialize(self) -> None:
        logger.info("Authorization Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Authorization Module Shutdown.")
