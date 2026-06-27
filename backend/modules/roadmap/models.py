from pydantic import BaseModel
from typing import List, Optional, Dict
from .enums import NodeType, NodeStatus, DependencyType

class RoadmapNodeDependency(BaseModel):
    node_id: str
    dependency_type: DependencyType = DependencyType.MANDATORY

class RoadmapNode(BaseModel):
    id: str
    title: str
    description: str
    type: NodeType
    learning_material_id: Optional[str] = None
    dependencies: List[RoadmapNodeDependency] = []
    metadata: Dict[str, str] = {} # E.g., Estimated Time

class RoadmapStage(BaseModel):
    id: str
    title: str
    order: int
    nodes: List[RoadmapNode]

class Roadmap(BaseModel):
    id: str
    title: str
    description: str
    stages: List[RoadmapStage]

class UserNodeProgress(BaseModel):
    node_id: str
    status: NodeStatus
    score: Optional[float] = None

class UserRoadmapProgress(BaseModel):
    user_id: str
    roadmap_id: str
    node_progress: Dict[str, UserNodeProgress] # Key is node_id
