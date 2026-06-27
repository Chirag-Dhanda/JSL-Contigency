from typing import List, Optional
from pydantic import BaseModel

from .enums import EmergencyType

class ContactRole(BaseModel):
    role_title: str
    contact_number: str
    order: int

class EmergencyProcedure(BaseModel):
    id: str
    type: EmergencyType
    title: str
    description: str
    immediate_actions: List[str] = []
    escalation_chain: List[ContactRole] = []
    required_ppe_ids: List[str] = []
    vr_simulation_id: Optional[str] = None # Future VR integration
    department_id: Optional[str] = None # For department-specific emergencies
