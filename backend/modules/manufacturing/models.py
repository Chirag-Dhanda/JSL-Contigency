from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum

from .enums import ManufacturingStageType, FlowDirection

class StationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    MAINTENANCE = "MAINTENANCE"
    OFFLINE = "OFFLINE"
    FUTURE = "FUTURE"

class ManufacturingStation(BaseModel):
    id: str
    name: str
    description: str
    purpose: str
    input_materials: List[str]
    output_materials: List[str]
    equipment: List[str]
    safety_precautions: List[str]
    quality_parameters: List[str]
    common_problems: List[str]
    
    # Hooks for future enterprise integrations
    scada_endpoint: Optional[str] = None
    sap_work_center_id: Optional[str] = None
    iot_sensors: List[str] = []
    
class DigitalFactoryJourney(BaseModel):
    id: str
    title: str
    stations: List[ManufacturingStation]
    
class EmployeeStationProgress(BaseModel):
    user_id: str
    station_id: str
    visited: bool = False
    time_spent_seconds: int = 0
    lessons_completed: int = 0

class FlowConnection(BaseModel):
    target_stage_id: str
    direction: FlowDirection
    description: Optional[str] = None

class ManufacturingStage(BaseModel):
    id: str
    name: str
    stage_type: ManufacturingStageType
    description: str
    order_index: int
    connections: List[FlowConnection] = []
    equipment_ids: List[str] = []
    department_id: Optional[str] = None
    media_asset_ids: List[str] = [] # Visual flowcharts or diagrams

class ProcessFlow(BaseModel):
    id: str
    name: str
    description: str
    stages: List[ManufacturingStage]
