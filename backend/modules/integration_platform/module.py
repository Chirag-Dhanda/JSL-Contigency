"""
DI Registration for Enterprise Integration Platform (EP-10).
"""
import logging
from typing import Any

from core.module import BaseModule
from core.di import container

from modules.governance_platform.governance_engine import GovernanceEngine

from .gateway import IntegrationGateway
from .transformation import TransformationEngine
from .sync_engine import IntegrationSyncEngine
from .scheduler import IntegrationScheduler
from .conflict_engine import ConflictResolutionEngine
from .review import IntegrationReviewService

logger = logging.getLogger("IntegrationPlatformModule")


class IntegrationPlatformModule(BaseModule):
    @property
    def name(self) -> str:
        return "IntegrationPlatform"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: Any) -> None:
        logger.info("Registering Integration Platform (EP-10) services...")

        gateway = IntegrationGateway()
        container.register_singleton(IntegrationGateway, gateway)

        transformation = TransformationEngine()
        container.register_singleton(TransformationEngine, transformation)

        conflict = ConflictResolutionEngine()
        container.register_singleton(ConflictResolutionEngine, conflict)

        sync_engine = IntegrationSyncEngine(gateway, transformation, conflict)
        container.register_singleton(IntegrationSyncEngine, sync_engine)

        scheduler = IntegrationScheduler(sync_engine)
        container.register_singleton(IntegrationScheduler, scheduler)

        gov_engine = container.resolve(GovernanceEngine)
        review_svc = IntegrationReviewService(gateway, gov_engine)
        container.register_singleton(IntegrationReviewService, review_svc)

    async def initialize(self) -> None:
        logger.info("Integration Platform initialized.")

    async def shutdown(self) -> None:
        pass
