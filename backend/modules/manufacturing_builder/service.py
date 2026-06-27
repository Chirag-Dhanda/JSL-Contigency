import logging
import uuid
from typing import Dict, List, Optional
from modules.process_modeling.models import ManufacturingFlow
from modules.process_runtime.engine import ProcessRuntimeEngine
from exceptions.base import NotFoundException

logger = logging.getLogger("ManufacturingBuilder")

class ManufacturingBuilderService:
    """
    Manages the lifecycle of Visual Manufacturing Flows in the Knowledge Studio.
    Provides AI suggestions for missing metadata.
    """
    
    def __init__(self, process_engine: ProcessRuntimeEngine):
        self.process_engine = process_engine
        self._flows: Dict[str, ManufacturingFlow] = {}
        logger.info("Manufacturing Builder Service Initialized.")
        
    def save_flow(self, flow: ManufacturingFlow) -> ManufacturingFlow:
        """Saves a draft visual flow."""
        self._flows[flow.id] = flow
        logger.info(f"Saved Manufacturing Flow: {flow.name}")
        return flow
        
    def get_flow(self, flow_id: str) -> ManufacturingFlow:
        if flow_id not in self._flows:
            raise NotFoundException(message=f"Flow {flow_id} not found.")
        return self._flows[flow_id]
        
    def list_flows(self) -> List[ManufacturingFlow]:
        return list(self._flows.values())
        
    def publish_flow(self, flow_id: str, user_id: str) -> ManufacturingFlow:
        """Compiles the flow into the core engines."""
        flow = self.get_flow(flow_id)
        self.process_engine.publish_flow(flow, user_id)
        return flow
        
    def get_ai_suggestions(self, flow_id: str) -> List[dict]:
        """
        Mock AI logic scanning a draft flow for missing links or anomalies.
        """
        flow = self.get_flow(flow_id)
        suggestions = []
        
        for node in flow.nodes:
            if not node.configuration.required_sops:
                suggestions.append({
                    "node_id": node.id,
                    "node_label": node.label,
                    "type": "MISSING_SOP",
                    "message": f"AI Suggestion: '{node.label}' has no linked SOPs. Consider linking a safety or procedure document."
                })
            
            if not node.equipment_ids:
                suggestions.append({
                    "node_id": node.id,
                    "node_label": node.label,
                    "type": "MISSING_EQUIPMENT",
                    "message": f"AI Suggestion: '{node.label}' has no equipment mapped. Is this a manual stage?"
                })
                
        return suggestions
