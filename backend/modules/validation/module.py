from core.module import BaseModule
from core.di import ServiceContainer
from .sanitizer import InputSanitizer
from .file_validator import FileValidator
from logging import getLogger

logger = getLogger("ValidationModule")

class ValidationModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Validation"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        logger.debug("Registering Validation Services...")
        # Static classes mostly, but we can register if they become stateful
        container.register_singleton(InputSanitizer, InputSanitizer())
        container.register_singleton(FileValidator, FileValidator())

    async def initialize(self) -> None:
        logger.info("Validation Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Validation Module Shutdown.")
