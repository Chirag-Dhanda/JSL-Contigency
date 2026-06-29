"""
Event Engine for Enterprise Workflow (EP-07).
Provides a simple in-process pub/sub mechanism for workflow-driven events.
"""
import logging
import asyncio
from typing import Dict, List, Callable, Awaitable, Any

from .models import WorkflowEvent

logger = logging.getLogger("WorkflowEngine.EventEngine")

# Type alias for an async event handler
EventHandler = Callable[[WorkflowEvent], Awaitable[None]]


class EventEngine:
    """
    Lightweight pub/sub event bus.
    Modules subscribe to event_type strings; the engine dispatches events to registered handlers.
    
    Future Extension: Replace internal handler list with Redis Pub/Sub or Kafka topics.
    """
    
    def __init__(self):
        self._handlers: Dict[str, List[EventHandler]] = {}

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Register a handler for the given event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        logger.debug(f"Subscribed handler '{handler.__name__}' to event '{event_type}'")

    async def emit(self, event: WorkflowEvent) -> None:
        """Emit an event, dispatching to all registered handlers."""
        handlers = self._handlers.get(event.event_type, [])
        if not handlers:
            logger.debug(f"No handlers for event type '{event.event_type}'")
            return
        
        logger.info(f"Emitting event '{event.event_type}' to {len(handlers)} handler(s)")
        tasks = [handler(event) for handler in handlers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Event handler {handlers[i].__name__} failed: {result}")


# Canonical event type strings — extensible, never hardcoded in business logic
class EventTypes:
    WORKFLOW_STARTED = "WORKFLOW_STARTED"
    WORKFLOW_COMPLETED = "WORKFLOW_COMPLETED"
    WORKFLOW_CANCELLED = "WORKFLOW_CANCELLED"
    TASK_CREATED = "TASK_CREATED"
    TASK_COMPLETED = "TASK_COMPLETED"
    APPROVAL_REQUESTED = "APPROVAL_REQUESTED"
    APPROVAL_GRANTED = "APPROVAL_GRANTED"
    APPROVAL_REJECTED = "APPROVAL_REJECTED"
    KNOWLEDGE_PUBLISHED = "KNOWLEDGE_PUBLISHED"
    OBJECT_CREATED = "OBJECT_CREATED"
    OBJECT_UPDATED = "OBJECT_UPDATED"
