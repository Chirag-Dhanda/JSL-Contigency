import logging
from typing import Dict, Any, List
from modules.relationship_engine.service import RelationshipEngineService

logger = logging.getLogger("ComplianceEngine")

class ComplianceEngineService:
    """
    Analyzes change impact and compliance violations before publishing.
    """
    def __init__(self, rel_engine: RelationshipEngineService):
        self.rel_engine = rel_engine
        logger.info("Compliance Engine Initialized.")

    def calculate_change_impact(self, entity_id: str) -> Dict[str, Any]:
        """
        Determines the ripple effect of changing or deprecating this entity.
        """
        logger.info(f"Calculating compliance impact for {entity_id}")
        
        rels = self.rel_engine.get_relationships_for_entity(entity_id)
        
        affected_sops = sum(1 for r in rels if r.relationship_type == "REQUIRES_SOP")
        affected_equipment = sum(1 for r in rels if r.relationship_type in ["USES_EQUIPMENT", "REQUIRES_EQUIPMENT"])
        affected_flows = sum(1 for r in rels if r.relationship_type == "NEXT_STAGE")
        
        warnings = []
        if affected_sops > 0:
            warnings.append(f"Modifying this entity may invalidate {affected_sops} linked SOPs.")
        if affected_flows > 0:
            warnings.append("This entity is part of an active Manufacturing Flow.")
            
        return {
            "entity_id": entity_id,
            "impact_score": "HIGH" if warnings else "LOW",
            "affected_sops": affected_sops,
            "affected_equipment": affected_equipment,
            "affected_flows": affected_flows,
            "compliance_warnings": warnings
        }
