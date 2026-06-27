from core.module import BaseModule
from core.di import ServiceContainer
from .bus import EventBus
from logging import getLogger

logger = getLogger("EventsModule")

class EventsModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Events"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        logger.debug("Registering EventBus as Singleton...")
        container.register_singleton(EventBus, EventBus())

    async def initialize(self) -> None:
        logger.info("Events Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Events Module Shutdown.")
