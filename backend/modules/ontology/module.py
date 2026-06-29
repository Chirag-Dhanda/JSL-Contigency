from core.module import BaseModule
from core.di import ServiceContainer
from .registry import OntologyRegistryService
from logging import getLogger

logger = getLogger("OntologyModule")

class OntologyModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Ontology"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        """Register Ontology services."""
        logger.debug("Registering Ontology Services...")
        container.register_singleton(OntologyRegistryService, OntologyRegistryService())

    async def initialize(self) -> None:
        logger.info("Ontology Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Ontology Module Shutdown.")
