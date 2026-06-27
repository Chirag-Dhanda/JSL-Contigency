from typing import Callable, Dict, List, Awaitable
from logging import getLogger
from .models import DomainEvent
import asyncio

logger = getLogger("EventBus")

# Type alias for event handlers
EventHandler = Callable[[DomainEvent], Awaitable[None]]

class EventBus:
    """Central Publish/Subscribe messaging layer."""
    
    def __init__(self):
        self._subscribers: Dict[str, List[EventHandler]] = {}
        
    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        logger.debug(f"Subscribed handler to {event_type}")

    async def publish(self, event: DomainEvent) -> None:
        handlers = self._subscribers.get(event.event_type, [])
        logger.info(f"Publishing {event.event_type} to {len(handlers)} handlers.")
        
        # Fire-and-forget execution of all handlers concurrently
        tasks = [asyncio.create_task(handler(event)) for handler in handlers]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
