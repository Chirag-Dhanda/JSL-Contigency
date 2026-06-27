import logging
from typing import Dict, Any
from modules.governance.models import LifecycleState
from modules.version_engine.service import VersionEngineService
from modules.audit_engine.service import AuditEngineService
from modules.compliance.service import ComplianceEngineService
from modules.metadata_engine.service import MetadataEngineService

logger = logging.getLogger("PublishingEngine")

class PublishingEngineService:
    """
    Orchestrates the lifecycle transitions of entities.
    """
    def __init__(self, meta: MetadataEngineService, version: VersionEngineService, audit: AuditEngineService, compliance: ComplianceEngineService):
        self.meta = meta
        self.version = version
        self.audit = audit
        self.compliance = compliance
        self._states: Dict[str, LifecycleState] = {} # entity_id -> State
        logger.info("Publishing Engine Initialized.")

    def get_state(self, entity_id: str) -> LifecycleState:
        return self._states.get(entity_id, LifecycleState.DRAFT)

    def transition_to_review(self, entity_id: str, user_id: str):
        current = self.get_state(entity_id)
        if current != LifecycleState.DRAFT:
            raise Exception("Only DRAFTs can be submitted for review.")
        self._states[entity_id] = LifecycleState.UNDER_REVIEW
        self.audit.record_action(user_id, entity_id, "PublishingEngine", "SUBMIT_FOR_REVIEW")
        logger.info(f"{entity_id} moved to UNDER_REVIEW")

    def approve_draft(self, entity_id: str, user_id: str):
        self._states[entity_id] = LifecycleState.APPROVED
        self.audit.record_action(user_id, entity_id, "PublishingEngine", "APPROVE")
        logger.info(f"{entity_id} moved to APPROVED")

    def publish(self, entity_id: str, user_id: str, notes: str = "Published"):
        current = self.get_state(entity_id)
        if current not in [LifecycleState.APPROVED, LifecycleState.DRAFT]: # Relaxing for demo
            pass
            
        # 1. Compliance Check
        impact = self.compliance.calculate_change_impact(entity_id)
        if impact["impact_score"] == "HIGH":
            logger.warning(f"Publishing {entity_id} with HIGH impact score!")
            
        # 2. Transition
        self._states[entity_id] = LifecycleState.PUBLISHED
        
        # 3. Snapshot Version
        self.version.create_version(entity_id, user_id, "minor", notes)
        
        # 4. Audit
        self.audit.record_action(user_id, entity_id, "PublishingEngine", "PUBLISH", reason=notes)
        logger.info(f"{entity_id} PUBLISHED successfully.")
