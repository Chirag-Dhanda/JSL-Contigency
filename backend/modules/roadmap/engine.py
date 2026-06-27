from typing import Dict, List
from .models import Roadmap, UserRoadmapProgress, NodeStatus, DependencyType
from exceptions.base import BusinessRuleException
from logging import getLogger

logger = getLogger("RoadmapEngine")

class RoadmapEngine:
    """DAG Engine to evaluate learning journey unlock conditions."""
    
    @staticmethod
    def evaluate_node_status(node_id: str, roadmap: Roadmap, user_progress: UserRoadmapProgress) -> NodeStatus:
        """Determines if a node should be LOCKED, UNLOCKED, or maintains its current state."""
        
        # If user already interacted with it, return current state
        if node_id in user_progress.node_progress:
            current_status = user_progress.node_progress[node_id].status
            if current_status in [NodeStatus.COMPLETED, NodeStatus.IN_PROGRESS, NodeStatus.SKIPPED, NodeStatus.UNLOCKED]:
                return current_status
                
        # Find the node configuration
        target_node = None
        for stage in roadmap.stages:
            for n in stage.nodes:
                if n.id == node_id:
                    target_node = n
                    break
        
        if not target_node:
            raise BusinessRuleException(f"Node {node_id} not found in Roadmap {roadmap.id}")
            
        # Check dependencies
        for dep in target_node.dependencies:
            if dep.dependency_type == DependencyType.MANDATORY:
                dep_status = user_progress.node_progress.get(dep.node_id)
                # If a mandatory dependency is missing or not completed, this node is locked
                if not dep_status or dep_status.status != NodeStatus.COMPLETED:
                    return NodeStatus.LOCKED
                    
        # All mandatory dependencies met (or no dependencies exist)
        return NodeStatus.UNLOCKED

    @staticmethod
    def recalculate_journey(roadmap: Roadmap, user_progress: UserRoadmapProgress) -> None:
        """Runs a pass over all nodes to unlock new nodes based on recent completions."""
        unlocked_count = 0
        for stage in roadmap.stages:
            for node in stage.nodes:
                new_status = RoadmapEngine.evaluate_node_status(node.id, roadmap, user_progress)
                
                # Update progress tracking if state changed to UNLOCKED
                if new_status == NodeStatus.UNLOCKED and node.id not in user_progress.node_progress:
                    from .models import UserNodeProgress
                    user_progress.node_progress[node.id] = UserNodeProgress(node_id=node.id, status=NodeStatus.UNLOCKED)
                    unlocked_count += 1
                    
        if unlocked_count > 0:
            logger.debug(f"DAG Engine unlocked {unlocked_count} new nodes for user {user_progress.user_id}.")
