from typing import List
from pydantic import BaseModel

class LinkedKnowledge(BaseModel):
    sop_id: str
    
    # Linked domain knowledge objects
    equipment_ids: List[str] = []
    manufacturing_stage_ids: List[str] = []
    safety_module_ids: List[str] = []
    assessment_ids: List[str] = []
    learning_module_ids: List[str] = []
    
    # Future SAP references
    sap_transaction_codes: List[str] = []
