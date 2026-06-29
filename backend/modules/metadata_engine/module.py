from core.module import BaseModule
from core.di import ServiceContainer
from .service import MetadataEngineService
from .pg_repository import PostgresMetadataRepository
from modules.schema_engine.validator import SchemaValidator
from logging import getLogger

logger = getLogger("MetadataEngineModule")

class MetadataEngineModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "MetadataEngine"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        """Register Metadata Engine services into the global DI container."""
        logger.debug("Registering Metadata Engine Services...")
        
        repository = PostgresMetadataRepository()
        validator = SchemaValidator()
        
        service = MetadataEngineService(repository=repository, validator=validator)
        container.register_singleton(MetadataEngineService, service)

    async def initialize(self) -> None:
        logger.info("Metadata Engine Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Metadata Engine Module Shutdown.")
