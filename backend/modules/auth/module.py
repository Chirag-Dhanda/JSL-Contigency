from core.module import BaseModule
from core.di import ServiceContainer
from .repository import IAuthRepository, MockAuthRepository
from .service import AuthService
from logging import getLogger

logger = getLogger("AuthModule")

class AuthModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Authentication"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        """Register Auth services into the global DI container."""
        logger.debug("Registering Auth Services...")
        
        # Register Repository
        container.register_singleton(IAuthRepository, MockAuthRepository())
        
        # Register Service, injecting the repository interface
        container.register_singleton(AuthService, AuthService())

    async def initialize(self) -> None:
        """Initialize the Auth module (placeholder for future cache/DB prep)."""
        logger.info("Authentication Module Initialized.")

    async def shutdown(self) -> None:
        """Shutdown the Auth module."""
        logger.info("Authentication Module Shutdown.")
