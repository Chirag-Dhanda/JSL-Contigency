from core.module import BaseModule
from core.di import ServiceContainer
from .service import NotificationService
from .dispatcher import DispatcherRegistry
from modules.templates.engine import TemplateEngine
from logging import getLogger

logger = getLogger("NotificationsModule")

class NotificationsModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Notifications"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        logger.debug("Registering Notifications Services...")
        dispatchers = DispatcherRegistry()
        container.register_singleton(DispatcherRegistry, dispatchers)
        
        # Service requires TemplateEngine, which is registered by TemplatesModule
        # We can resolve it dynamically inside a factory or resolve it during instantiation if it's already registered.
        # Since main.py dictates registration order, TemplatesModule must be registered before NotificationsModule.
        templates = container.resolve(TemplateEngine)
        container.register_singleton(NotificationService, NotificationService(templates, dispatchers))

    async def initialize(self) -> None:
        logger.info("Notifications Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Notifications Module Shutdown.")
