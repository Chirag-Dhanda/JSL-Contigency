from core.module import BaseModule
from logging import getLogger

logger = getLogger("MiddlewareModule")

class MiddlewareModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Middleware"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container) -> None:
        pass

    async def initialize(self) -> None:
        logger.info("Enterprise Middleware Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Enterprise Middleware Module Shutdown.")
