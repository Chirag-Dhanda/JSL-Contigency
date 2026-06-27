from typing import Callable, Dict, List, Any
from logging import getLogger
import asyncio

logger = getLogger("EventDispatcher")

class ApplicationEvents:
    APP_STARTING = "app.starting"
    CONFIG_LOADED = "app.config_loaded"
    MODULES_REGISTERED = "app.modules_registered"
    APP_READY = "app.ready"
    APP_SHUTTING_DOWN = "app.shutting_down"

class EventDispatcher:
    """Asynchronous internal event Pub/Sub dispatcher."""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[..., Any]]] = {}

    def subscribe(self, event_name: str, handler: Callable[..., Any]) -> None:
        """Subscribe a handler to an event."""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)
        logger.trace(f"Subscribed handler {handler.__name__} to event: {event_name}")

    async def dispatch(self, event_name: str, *args, **kwargs) -> None:
        """Dispatch an event asynchronously to all subscribers."""
        if event_name not in self._subscribers:
            logger.trace(f"No subscribers for event: {event_name}")
            return
            
        logger.debug(f"Dispatching Event: {event_name}")
        tasks = []
        for handler in self._subscribers[event_name]:
            if asyncio.iscoroutinefunction(handler):
                tasks.append(handler(*args, **kwargs))
            else:
                # Run synchronous handlers normally, though ideally they should be async
                try:
                    handler(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Event handler {handler.__name__} failed on {event_name}: {e}")
                    
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Async event handler failed on {event_name}: {result}")

# Global Event Dispatcher
event_dispatcher = EventDispatcher()
