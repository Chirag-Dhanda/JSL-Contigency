from typing import List, Optional
from pydantic import BaseModel

from .enums import SafetyCategory, HazardLevel, PPEType

class PPEItem(BaseModel):
    id: str
    ppe_type: PPEType
    name: str
    description: str
    purpose: str
    inspection_checklist: List[str] = []
    replacement_criteria: List[str] = []
    media_asset_ids: List[str] = []

class Hazard(BaseModel):
    id: str
    category: SafetyCategory
    name: str
    description: str
    risk_level: HazardLevel
    preventive_measures: List[str] = []
    control_measures: List[str] = []
    required_ppe_ids: List[str] = []
    safety_signage_asset_ids: List[str] = []
    near_miss_examples: List[str] = []

class SafetyModule(BaseModel):
    id: str
    category: SafetyCategory
    title: str
    description: str
    related_hazard_ids: List[str] = []
    mandatory_assessment_id: Optional[str] = None
    
    # Future AI Integration Hooks
    ai_safety_coach_prompt: Optional[str] = None
    # Future SCADA integration
    iot_sensor_triggers: List[str] = []
