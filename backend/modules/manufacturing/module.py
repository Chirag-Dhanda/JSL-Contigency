from core.module import BaseModule
from core.di import ServiceContainer
from .service import ManufacturingService
from logging import getLogger

logger = getLogger("ManufacturingModule")

class ManufacturingModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Manufacturing"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        logger.debug("Registering Manufacturing Service...")
        self.svc = ManufacturingService()
        container.register_singleton(ManufacturingService, self.svc)

    async def initialize(self) -> None:
        # Pre-build the default manufacturing journey for the platform
        self.svc.build_default_stainless_steel_journey()
        logger.info("Manufacturing Module Initialized with default SS Journey.")

    async def shutdown(self) -> None:
        logger.info("Manufacturing Module Shutdown.")
