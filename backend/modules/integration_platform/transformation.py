"""
Data Transformation Engine (EP-10).
Converts vendor-specific payloads to EKOS structures using metadata mapping rules.
"""
import logging
from typing import Dict, Any, List, Optional

from .models import MappingRule, FieldMapping

logger = logging.getLogger("Integration.Transformation")


class TransformationEngine:
    def __init__(self):
        self._mappings: Dict[str, MappingRule] = {}

    def register_mapping(self, mapping: MappingRule) -> None:
        self._mappings[mapping.mapping_id] = mapping
        logger.info(f"Registered mapping {mapping.mapping_id} for {mapping.source_entity} -> {mapping.target_entity}")

    def get_mappings_for_connector(self, connector_id: str) -> List[MappingRule]:
        return [m for m in self._mappings.values() if m.connector_id == connector_id]

    def transform_inbound(self, payload_data: Dict[str, Any], mapping: MappingRule) -> Dict[str, Any]:
        """
        Transforms data coming FROM an external system INTO an EKOS structure.
        """
        result = {}
        for field_map in mapping.fields:
            if field_map.source_field in payload_data:
                val = payload_data[field_map.source_field]
                result[field_map.target_field] = self._apply_rule(val, field_map.transform_rule)
                
        # In a full implementation, this would also handle schema validation 
        # and generating relationships based on foreign keys.
        return result

    def transform_outbound(self, ekos_data: Dict[str, Any], mapping: MappingRule) -> Dict[str, Any]:
        """
        Transforms data coming FROM EKOS OUT to an external system.
        """
        result = {}
        for field_map in mapping.fields:
            if field_map.target_field in ekos_data:
                val = ekos_data[field_map.target_field]
                result[field_map.source_field] = val # Outbound transformations omitted for brevity
        return result

    def _apply_rule(self, value: Any, rule: Optional[str]) -> Any:
        if not rule or value is None:
            return value
            
        rule = rule.upper()
        try:
            if rule == "UPPER":
                return str(value).upper()
            elif rule == "LOWER":
                return str(value).lower()
            elif rule == "TO_STRING":
                return str(value)
            elif rule == "TO_INT":
                return int(value)
            elif rule == "TO_FLOAT":
                return float(value)
            elif rule == "ISO_DATE":
                # Very naive date parsing mock
                return str(value)
            else:
                logger.warning(f"Unknown transform rule: {rule}")
                return value
        except Exception as e:
            logger.error(f"Transformation error on {value} with rule {rule}: {e}")
            raise ValueError(f"Failed to transform {value} using {rule}")
