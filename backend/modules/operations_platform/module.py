"""
DI Registration for Enterprise Operations Platform (EP-12).
"""
import logging
from typing import Any

from core.module import BaseModule
from core.di import container

from modules.governance_platform.governance_engine import GovernanceEngine

from .health import HealthManager
from .telemetry import TelemetryEngine
from .alerts import AlertEngine
from .diagnostics import DiagnosticsEngine
from .backup import BackupManager

logger = logging.getLogger("OperationsPlatformModule")


class OperationsPlatformModule(BaseModule):
    @property
    def name(self) -> str:
        return "OperationsPlatform"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: Any) -> None:
        logger.info("Registering Enterprise Operations Platform (EP-12) services...")

        health = HealthManager()
        container.register_singleton(HealthManager, health)

        telemetry = TelemetryEngine()
        container.register_singleton(TelemetryEngine, telemetry)

        alerts = AlertEngine()
        container.register_singleton(AlertEngine, alerts)

        diagnostics = DiagnosticsEngine(telemetry)
        container.register_singleton(DiagnosticsEngine, diagnostics)

        gov_engine = container.resolve(GovernanceEngine)
        backup = BackupManager(gov_engine)
        container.register_singleton(BackupManager, backup)

    async def initialize(self) -> None:
        logger.info("Enterprise Operations Platform initialized.")
        
        # In a full implementation, we would register the health checks here
        health = container.resolve(HealthManager)
        
        async def mock_db_check():
            from .models import ComponentHealth, HealthStatus
            return ComponentHealth(component_name="Database", status=HealthStatus.OK)
            
        health.register_component("Database", mock_db_check)

    async def shutdown(self) -> None:
        pass
