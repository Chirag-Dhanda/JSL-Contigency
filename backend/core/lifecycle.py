from typing import List, Type
from logging import getLogger
from config.manager import get_config
from core.di import container, ServiceContainer
from core.events import event_dispatcher, ApplicationEvents
from core.module import BaseModule
from exceptions.base import SystemException

logger = getLogger("LifecycleManager")

class ApplicationManager:
    """Enterprise Application Lifecycle Manager."""
    
    def __init__(self):
        self._modules: List[BaseModule] = []
        self._is_ready = False

    def register_module(self, module_class: Type[BaseModule]) -> None:
        """Instantiate and register a module into the lifecycle."""
        if self._is_ready:
            raise SystemException("Cannot register modules after the application has started.")
        
        module = module_class()
        self._modules.append(module)
        logger.info(f"Registered Module: {module.name} (v{module.version})")

    async def startup(self) -> None:
        """Executes the strict application startup sequence."""
        logger.info("Initializing Enterprise Application Lifecycle...")
        await event_dispatcher.dispatch(ApplicationEvents.APP_STARTING)
        
        # 1. Configuration Check
        config = get_config()
        await event_dispatcher.dispatch(ApplicationEvents.CONFIG_LOADED, config=config)
        logger.debug("Configuration verified.")
        
        # 2. Service Registration Phase
        logger.debug("Registering module services into IoC container...")
        for module in self._modules:
            module.register_services(container)
        await event_dispatcher.dispatch(ApplicationEvents.MODULES_REGISTERED, container=container)
            
        # 3. Initialization Phase
        logger.debug("Initializing modules...")
        for module in self._modules:
            await module.initialize()
            
        # 4. Ready State
        self._is_ready = True
        logger.info("Enterprise Application Lifecycle Ready.")
        await event_dispatcher.dispatch(ApplicationEvents.APP_READY)

    async def shutdown(self) -> None:
        """Executes the strict application shutdown sequence."""
        logger.info("Commencing Enterprise Application Graceful Shutdown...")
        await event_dispatcher.dispatch(ApplicationEvents.APP_SHUTTING_DOWN)
        
        # Shutdown modules in reverse order
        for module in reversed(self._modules):
            logger.debug(f"Shutting down module: {module.name}")
            await module.shutdown()
            
        container.clear()
        logger.info("Application Shutdown Complete.")

# Global Lifecycle Manager
lifecycle = ApplicationManager()
