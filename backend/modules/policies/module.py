from core.module import BaseModule
from core.di import ServiceContainer
from .engine import PolicyEngine
from logging import getLogger

logger = getLogger("PoliciesModule")

class PoliciesModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Policies"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        logger.debug("Registering Policy Engine...")
        container.register_singleton(PolicyEngine, PolicyEngine())

    async def initialize(self) -> None:
        logger.info("Policies Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Policies Module Shutdown.")
