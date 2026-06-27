from typing import List, Optional
from pydantic import BaseModel

from .enums import EquipmentStatus, EngineeringDataType

class EngineeringParameter(BaseModel):
    name: str
    data_type: EngineeringDataType
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    unit: str
    # Future SCADA integration
    scada_tag_id: Optional[str] = None
    is_live: bool = False

class EquipmentRelationship(BaseModel):
    related_sops: List[str] = []
    related_lessons: List[str] = []
    related_assessments: List[str] = []
    safety_procedures: List[str] = []
    related_equipment_ids: List[str] = []

class AIHooks(BaseModel):
    # Placeholders for future generative triggers
    explain_like_beginner_prompt: Optional[str] = None
    explain_like_engineer_prompt: Optional[str] = None
    maintenance_summary_prompt: Optional[str] = None
    revision_questions_prompt: Optional[str] = None

class EquipmentKnowledge(BaseModel):
    id: str
    name: str
    status: EquipmentStatus
    purpose: str
    operating_principle: str
    input_materials: List[str] = []
    output_materials: List[str] = []
    technical_specifications: List[str] = []
    
    # Deep Knowledge
    common_failures: List[str] = []
    troubleshooting_steps: List[str] = []
    preventive_maintenance: List[str] = []
    inspection_checklist: List[str] = []
    quality_checks: List[str] = []
    
    # Data Architecture
    engineering_parameters: List[EngineeringParameter] = []
    relationships: EquipmentRelationship
    ai_hooks: AIHooks
    
    # Metadata
    department_id: Optional[str] = None
    media_asset_ids: List[str] = [] # 3D models, diagrams, images
    sap_equipment_id: Optional[str] = None
