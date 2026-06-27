from typing import Dict, Optional
from .models import Roadmap, UserRoadmapProgress, NodeStatus, UserNodeProgress
from .engine import RoadmapEngine
from exceptions.base import NotFoundException
from logging import getLogger

logger = getLogger("RoadmapService")

class RoadmapService:
    def __init__(self):
        # Mock Databases
        self._roadmaps: Dict[str, Roadmap] = {}
        self._user_progress: Dict[str, UserRoadmapProgress] = {}
        
    def register_roadmap(self, roadmap: Roadmap):
        self._roadmaps[roadmap.id] = roadmap
        
    def get_roadmap(self, roadmap_id: str) -> Roadmap:
        if roadmap_id not in self._roadmaps:
            raise NotFoundException(f"Roadmap {roadmap_id} not found.")
        return self._roadmaps[roadmap_id]
        
    def initialize_user_journey(self, user_id: str, roadmap_id: str) -> UserRoadmapProgress:
        """Assigns a roadmap to a user and initializes the first nodes as UNLOCKED."""
        roadmap = self.get_roadmap(roadmap_id)
        
        progress = UserRoadmapProgress(
            user_id=user_id,
            roadmap_id=roadmap_id,
            node_progress={}
        )
        
        # Run engine to unlock initial nodes with 0 dependencies
        RoadmapEngine.recalculate_journey(roadmap, progress)
        self._user_progress[f"{user_id}_{roadmap_id}"] = progress
        logger.info(f"Initialized Roadmap {roadmap_id} for user {user_id}")
        return progress

    def get_user_progress(self, user_id: str, roadmap_id: str) -> UserRoadmapProgress:
        key = f"{user_id}_{roadmap_id}"
        if key not in self._user_progress:
            raise NotFoundException("User journey not found.")
        return self._user_progress[key]

    def mark_node_completed(self, user_id: str, roadmap_id: str, node_id: str, score: Optional[float] = None) -> UserRoadmapProgress:
        """Marks a node as completed and triggers the DAG engine to unlock downstream nodes."""
        progress = self.get_user_progress(user_id, roadmap_id)
        roadmap = self.get_roadmap(roadmap_id)
        
        if node_id not in progress.node_progress:
            raise NotFoundException(f"Node {node_id} is not accessible for this user yet (Locked).")
            
        current = progress.node_progress[node_id]
        if current.status == NodeStatus.COMPLETED:
            logger.warning(f"Node {node_id} already completed for {user_id}.")
            return progress
            
        current.status = NodeStatus.COMPLETED
        current.score = score
        logger.info(f"User {user_id} COMPLETED node {node_id} on roadmap {roadmap_id}")
        
        # Trigger DAG Evaluation
        RoadmapEngine.recalculate_journey(roadmap, progress)
        
        return progress
