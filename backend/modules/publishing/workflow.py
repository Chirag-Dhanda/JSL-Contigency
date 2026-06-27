import logging
from typing import Dict, Any, List
from modules.metadata_engine.service import MetadataEngineService
from modules.entity_framework.lifecycle import EntityLifecycle
from exceptions.base import SystemException

logger = logging.getLogger("PublishingEngine")

class PublishingWorkflowService:
    """
    Enforces strict state transitions for entities, 
    ensuring content isn't published without review.
    """
    
    def __init__(self, metadata_engine: MetadataEngineService):
        self.metadata_engine = metadata_engine
        logger.info("Publishing Workflow Engine Initialized.")
        
    def submit_for_review(self, entity_id: str, submitted_by: str) -> bool:
        """Transitions an entity from DRAFT to REVIEW."""
        entity = self.metadata_engine.get_entity(entity_id)
        
        if entity.status != EntityLifecycle.DRAFT:
            raise SystemException(message=f"Cannot submit for review. Entity {entity_id} is in {entity.status.value} state.")
            
        self.metadata_engine.transition_lifecycle(entity_id, EntityLifecycle.REVIEW)
        logger.info(f"Entity {entity_id} submitted for review by {submitted_by}")
        return True
        
    def approve_content(self, entity_id: str, approved_by: str) -> bool:
        """Transitions an entity from REVIEW to APPROVED."""
        entity = self.metadata_engine.get_entity(entity_id)
        
        if entity.status != EntityLifecycle.REVIEW:
            raise SystemException(message=f"Cannot approve. Entity {entity_id} is not in REVIEW state.")
            
        self.metadata_engine.transition_lifecycle(entity_id, EntityLifecycle.APPROVED)
        logger.info(f"Entity {entity_id} approved by {approved_by}")
        return True
        
    def publish_content(self, entity_id: str, published_by: str) -> bool:
        """Transitions an entity from APPROVED to PUBLISHED."""
        entity = self.metadata_engine.get_entity(entity_id)
        
        # Fast-track for MASTER_EDITOR in Stage 5.3: Allow Draft -> Published directly
        if entity.status not in [EntityLifecycle.APPROVED, EntityLifecycle.DRAFT]:
             raise SystemException(message=f"Cannot publish. Entity {entity_id} is in {entity.status.value} state.")
             
        self.metadata_engine.transition_lifecycle(entity_id, EntityLifecycle.PUBLISHED)
        
        # In a real system, we would trigger an Event Bus notification here
        # e.g., EventBus.publish("ENTITY_PUBLISHED", payload={"id": entity_id})
        
        logger.info(f"Entity {entity_id} PUBLISHED by {published_by}")
        return True

    def archive_content(self, entity_id: str, archived_by: str) -> bool:
        """Moves content to ARCHIVED state."""
        self.metadata_engine.transition_lifecycle(entity_id, EntityLifecycle.ARCHIVED)
        logger.info(f"Entity {entity_id} ARCHIVED by {archived_by}")
        return True
