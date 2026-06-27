from core.module import BaseModule
from core.di import ServiceContainer
from .jwt import JWTService
from .hashing import PasswordHasher
from .password_recovery import PasswordRecoveryService
from .security_controls import AccountLockoutService
from .rate_limiter import RateLimiter
from logging import getLogger

logger = getLogger("SecurityModule")

class SecurityModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Security"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        """Register Security services into the global DI container."""
        logger.debug("Registering Security Services...")
        
        container.register_singleton(PasswordHasher, PasswordHasher())
        container.register_singleton(JWTService, JWTService())
        container.register_singleton(PasswordRecoveryService, PasswordRecoveryService())
        container.register_singleton(AccountLockoutService, AccountLockoutService())
        container.register_singleton(RateLimiter, RateLimiter())

    async def initialize(self) -> None:
        logger.info("Security Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Security Module Shutdown.")
