"""
Integration Review & Governance Integration (EP-10).
Bridges EIP to Governance Platform.
"""
import logging
from typing import Dict, Any

from .models import IntegrationReviewPackage, ConnectorDefinition, ConnectorStatus
from .gateway import IntegrationGateway
from modules.governance_platform.governance_engine import GovernanceEngine
from modules.governance_platform.models import GovernanceChangeType

logger = logging.getLogger("Integration.Review")


class IntegrationReviewService:
    def __init__(self, gateway: IntegrationGateway, gov_engine: GovernanceEngine):
        self._gateway = gateway
        self._gov_engine = gov_engine

    def propose_connector_activation(self, connector_id: str, proposed_by: str) -> str:
        """
        Creates a governance package proposing to activate a connector.
        Returns the governance package ID.
        """
        definition = self._gateway._definitions.get(connector_id)
        if not definition:
            raise ValueError(f"Connector {connector_id} not found.")
            
        if definition.status == ConnectorStatus.ACTIVE:
            raise ValueError(f"Connector {connector_id} is already ACTIVE.")

        # In a real scenario, this would gather test sync results and mapping proofs
        impact_analysis = f"Activating {definition.provider} connector. Will allow delta syncs to pull data into EKOS."
        
        gov_pkg = self._gov_engine.propose_change(
            change_type=GovernanceChangeType.WORKFLOW_GOVERNANCE, # Close enough for integration
            proposed_by=proposed_by,
            description=f"Activate Connector: {definition.name}",
            proposed_state={"connector_id": connector_id, "status": "ACTIVE"},
            current_state={"connector_id": connector_id, "status": definition.status.value},
            impact_analysis=impact_analysis
        )
        
        logger.info(f"Proposed activation of connector {connector_id}. Package ID: {gov_pkg.package_id}")
        return gov_pkg.package_id

    def apply_approved_package(self, package_id: str) -> None:
        """
        In a full implementation, the Governance Engine would emit an event when 
        a package is approved, and this service would listen and apply the changes.
        For this mock, it can be called explicitly.
        """
        gov_pkg = self._gov_engine.get_package(package_id)
        if not gov_pkg or gov_pkg.status.value != "APPROVED":
            logger.warning(f"Cannot apply unapproved package {package_id}")
            return
            
        props = gov_pkg.proposed_state
        connector_id = props.get("connector_id")
        target_status = props.get("status")
        
        if connector_id and target_status == "ACTIVE":
            definition = self._gateway._definitions.get(connector_id)
            if definition:
                definition.status = ConnectorStatus.ACTIVE
                logger.info(f"Applied governance approval: Connector {connector_id} is now ACTIVE.")
