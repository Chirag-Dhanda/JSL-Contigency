"""
Event Store for persistence and replay (EP-11).
"""
import logging
from typing import List, Optional
from datetime import datetime

from .models import DomainEvent

logger = logging.getLogger("Event.Store")


class IEventStore:
    def append(self, event: DomainEvent) -> None:
        raise NotImplementedError

    def get_events_since(self, timestamp: datetime) -> List[DomainEvent]:
        raise NotImplementedError
        
    def get_events_by_type(self, event_type: str) -> List[DomainEvent]:
        raise NotImplementedError


class InMemoryEventStore(IEventStore):
    """
    In-memory ledger of all events published through the bus.
    Serves as the foundation for event sourcing and replay capabilities.
    """
    def __init__(self):
        self._ledger: List[DomainEvent] = []

    def append(self, event: DomainEvent) -> None:
        self._ledger.append(event)
        logger.debug(f"Stored event {event.event_id} ({event.event_type})")

    def get_events_since(self, timestamp: datetime) -> List[DomainEvent]:
        return [e for e in self._ledger if e.timestamp >= timestamp]
        
    def get_events_by_type(self, event_type: str) -> List[DomainEvent]:
        return [e for e in self._ledger if e.event_type == event_type]
