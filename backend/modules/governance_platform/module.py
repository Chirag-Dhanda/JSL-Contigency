"""
DI Registration for Enterprise Governance Platform (EP-09).
"""
import logging
from typing import Any

from core.module import BaseModule
from core.di import container

from modules.audit.service import AuditService

from .policy_engine import EnterprisePolicyEngine
from .rls_engine import RowLevelSecurityEngine
from .field_security import FieldSecurityService
from .classification import ClassificationService
from .security_monitor import SecurityMonitor
from .compliance import ComplianceFramework
from .governance_engine import GovernanceEngine
from .audit_platform import EnterpriseAuditPlatform

logger = logging.getLogger("GovernancePlatformModule")


class GovernancePlatformModule(BaseModule):
    @property
    def name(self) -> str:
        return "GovernancePlatform"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: Any) -> None:
        logger.info("Registering Governance Platform (EP-09) services...")

        # Security Monitor
        monitor = SecurityMonitor()
        container.register_singleton(SecurityMonitor, monitor)

        # Policy Engine
        policy_engine = EnterprisePolicyEngine()
        container.register_singleton(EnterprisePolicyEngine, policy_engine)

        # RLS Engine
        rls_engine = RowLevelSecurityEngine()
        container.register_singleton(RowLevelSecurityEngine, rls_engine)

        # Field Security
        field_security = FieldSecurityService()
        container.register_singleton(FieldSecurityService, field_security)

        # Classification
        classification = ClassificationService()
        container.register_singleton(ClassificationService, classification)

        # Compliance
        compliance = ComplianceFramework()
        container.register_singleton(ComplianceFramework, compliance)

        # Governance Engine (Human in the loop)
        gov_engine = GovernanceEngine(security_monitor=monitor)
        container.register_singleton(GovernanceEngine, gov_engine)

        # Audit Platform
        raw_audit = container.resolve(AuditService)
        audit_platform = EnterpriseAuditPlatform(raw_audit_service=raw_audit)
        container.register_singleton(EnterpriseAuditPlatform, audit_platform)

    async def initialize(self) -> None:
        logger.info("Governance Platform initialized.")

    async def shutdown(self) -> None:
        pass
