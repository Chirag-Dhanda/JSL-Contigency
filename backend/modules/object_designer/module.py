from core.module import BaseModule
from core.di import ServiceContainer
from .service import ObjectDesignerService
from modules.metadata_engine.service import MetadataEngineService
from logging import getLogger

logger = getLogger("ObjectDesignerModule")

class ObjectDesignerModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "ObjectDesigner"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        """Register Object Designer services into the global DI container."""
        logger.debug("Registering Object Designer Services...")
        
        # Resolve dependencies (MetadataEngineService must be registered before this)
        metadata_engine = container.resolve(MetadataEngineService)
        
        service = ObjectDesignerService(metadata_engine=metadata_engine)
        container.register_singleton(ObjectDesignerService, service)

    async def initialize(self) -> None:
        logger.info("Object Designer Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Object Designer Module Shutdown.")
