"""
DI Registration for Enterprise Event Platform (EP-11).
"""
import logging
from typing import Any

from core.module import BaseModule
from core.di import container

from modules.governance_platform.governance_engine import GovernanceEngine

from .registry import EventRegistry
from .store import IEventStore, InMemoryEventStore
from .dlq import IDLQStorage, InMemoryDLQ
from .bus import AdvancedEventBus
from .subscription_engine import SubscriptionEngine
from .automation_engine import AutomationEngine

logger = logging.getLogger("EventPlatformModule")


class EventPlatformModule(BaseModule):
    @property
    def name(self) -> str:
        return "EventPlatform"

    @property
    def version(self) -> str:
        return "2.0.0"

    def register_services(self, container: Any) -> None:
        logger.info("Registering Enterprise Event Platform (EP-11) services...")

        registry = EventRegistry()
        container.register_singleton(EventRegistry, registry)

        # Persistence layers (abstracted so they can be swapped for DB later)
        store = InMemoryEventStore()
        container.register_singleton(IEventStore, store)

        dlq = InMemoryDLQ()
        container.register_singleton(IDLQStorage, dlq)

        # Bus
        bus = AdvancedEventBus(registry, store, dlq)
        # Note: We register it as AdvancedEventBus for EP-11 specific injections,
        # and as the original EventBus string name if older modules depend on it via name.
        container.register_singleton(AdvancedEventBus, bus)

        # Engines
        subscription = SubscriptionEngine(bus)
        container.register_singleton(SubscriptionEngine, subscription)

        automation = AutomationEngine(bus)
        container.register_singleton(AutomationEngine, automation)

    async def initialize(self) -> None:
        logger.info("Enterprise Event Platform initialized.")

    async def shutdown(self) -> None:
        pass
