"""
Enterprise Event Bus (EP-11).
Central Publish/Subscribe messaging layer with persistence and DLQ integration.
"""
from typing import Callable, Dict, List, Awaitable, Any
from logging import getLogger
import asyncio
import traceback

from .models import DomainEvent, DLQRecord
from .registry import EventRegistry
from .store import IEventStore
from .dlq import IDLQStorage

logger = getLogger("EventBus")

# Type alias for event handlers
EventHandler = Callable[[DomainEvent], Awaitable[None]]


class AdvancedEventBus:
    """Enterprise-grade Event Bus with persistence, retries, and dead-lettering."""
    
    def __init__(self, registry: EventRegistry, store: IEventStore, dlq: IDLQStorage):
        self._registry = registry
        self._store = store
        self._dlq = dlq
        self._subscribers: Dict[str, List[Dict[str, Any]]] = {} # event_type -> [{"name": str, "handler": callable}]

    def subscribe(self, event_type: str, subscriber_name: str, handler: EventHandler) -> None:
        """Register a handler for a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        self._subscribers[event_type].append({
            "name": subscriber_name,
            "handler": handler
        })
        logger.debug(f"Subscribed '{subscriber_name}' to {event_type}")

    async def publish(self, event: DomainEvent) -> None:
        """Publish an event, persisting it first, then dispatching to handlers."""
        # 1. Validate Schema
        is_valid = self._registry.validate_payload(event.event_type, event.version, event.payload)
        if not is_valid:
            logger.warning(f"Event {event.event_id} failed schema validation. Dropping.")
            return

        # 2. Persist to Event Store (At-least-once ledger)
        self._store.append(event)
        
        # 3. Dispatch
        handlers = self._subscribers.get(event.event_type, [])
        if not handlers:
            logger.debug(f"No subscribers for {event.event_type}")
            return
            
        logger.info(f"Publishing {event.event_type} to {len(handlers)} subscribers.")
        
        # Dispatch concurrently
        tasks = [
            asyncio.create_task(self._safe_dispatch(sub["name"], sub["handler"], event))
            for sub in handlers
        ]
        
        if tasks:
            await asyncio.gather(*tasks)

    async def _safe_dispatch(self, subscriber_name: str, handler: EventHandler, event: DomainEvent) -> None:
        """Executes a handler with retry logic and dead-letter queue routing."""
        max_retries = 3
        backoff_base_ms = 1000

        for attempt in range(max_retries):
            try:
                await handler(event)
                return  # Success
            except Exception as e:
                logger.warning(f"Error in subscriber '{subscriber_name}' for event {event.event_id} (Attempt {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    # Exponential backoff
                    sleep_time = (backoff_base_ms * (2 ** attempt)) / 1000.0
                    await asyncio.sleep(sleep_time)
                else:
                    # Terminal failure -> Route to DLQ
                    logger.error(f"Terminal failure for '{subscriber_name}' on event {event.event_id}. Routing to DLQ.")
                    dlq_record = DLQRecord(
                        event=event,
                        subscriber_name=subscriber_name,
                        error_message=str(e),
                        stack_trace=traceback.format_exc(),
                        retry_count=max_retries
                    )
                    self._dlq.add(dlq_record)
