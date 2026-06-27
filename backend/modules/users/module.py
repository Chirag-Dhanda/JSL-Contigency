from core.module import BaseModule
from core.di import ServiceContainer
from .service import EmployeeDirectoryService, ManagerService, ValidationService
from logging import getLogger

logger = getLogger("UsersModule")

class UsersModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Users"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        """Register User Domain services into the global DI container."""
        logger.debug("Registering Users Services...")
        
        container.register_singleton(EmployeeDirectoryService, EmployeeDirectoryService())
        container.register_singleton(ManagerService, ManagerService())
        container.register_singleton(ValidationService, ValidationService())

    async def initialize(self) -> None:
        logger.info("Users Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Users Module Shutdown.")
