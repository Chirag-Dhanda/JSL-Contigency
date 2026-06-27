from typing import Dict, List, Optional
from datetime import datetime, timezone
from .models import KnowledgeObject, ContentGroup
from .enums import ContentStatus
from exceptions.base import NotFoundException, BusinessRuleException
from logging import getLogger

logger = getLogger("KnowledgeService")

class KnowledgeService:
    def __init__(self):
        self._objects: Dict[str, KnowledgeObject] = {}
        self._groups: Dict[str, ContentGroup] = {}
        
    def create_knowledge_object(self, obj: KnowledgeObject) -> KnowledgeObject:
        """Authors a new piece of knowledge."""
        if obj.id in self._objects:
            raise BusinessRuleException(f"Knowledge Object {obj.id} already exists.")
        
        self._objects[obj.id] = obj
        logger.info(f"Authored new Knowledge Object: {obj.title} (Status: {obj.status.value})")
        return obj
        
    def get_knowledge_object(self, object_id: str) -> KnowledgeObject:
        if object_id not in self._objects:
            raise NotFoundException(f"Knowledge Object {object_id} not found.")
        return self._objects[object_id]
        
    def transition_status(self, object_id: str, new_status: ContentStatus, user_id: str) -> KnowledgeObject:
        """Workflow engine to move content through Draft -> Review -> Published -> Archived"""
        obj = self.get_knowledge_object(object_id)
        
        # Simple lifecycle simulation
        old_status = obj.status
        obj.status = new_status
        obj.updated_at = datetime.now(timezone.utc)
        
        logger.debug(f"Knowledge Object {object_id} transitioned from {old_status.value} to {new_status.value} by {user_id}")
        return obj

    def clone_as_draft(self, object_id: str, new_version: str, user_id: str) -> KnowledgeObject:
        """Clones an existing object as a new draft version."""
        original = self.get_knowledge_object(object_id)
        
        # In a real system, we'd assign a new ID and link to the original
        cloned_id = f"{original.id}-v{new_version}"
        if cloned_id in self._objects:
            raise BusinessRuleException(f"Version {new_version} already exists.")
            
        cloned_obj = original.model_copy(update={
            "id": cloned_id,
            "version": new_version,
            "status": ContentStatus.DRAFT,
            "author_id": user_id,
            "updated_at": datetime.now(timezone.utc)
        })
        self._objects[cloned_id] = cloned_obj
        logger.info(f"Cloned Knowledge Object {object_id} to new draft version {new_version}")
        return cloned_obj

    def create_content_group(self, group: ContentGroup) -> ContentGroup:
        """Creates a new content organization group."""
        if group.id in self._groups:
            raise BusinessRuleException(f"Content Group {group.id} already exists.")
        
        self._groups[group.id] = group
        logger.info(f"Created Content Group: {group.title} ({group.organization_type.value})")
        return group
        
    def get_content_group(self, group_id: str) -> ContentGroup:
        if group_id not in self._groups:
            raise NotFoundException(f"Content Group {group_id} not found.")
        return self._groups[group_id]

    def search_knowledge(self, query: str = "", tags: List[str] = None, department: str = None, role: str = None) -> List[KnowledgeObject]:
        """Mock search abstraction representing future semantic/AI indexing."""
        results = []
        for obj in self._objects.values():
            if obj.status != ContentStatus.PUBLISHED:
                continue
                
            match = True
            if query and query.lower() not in obj.title.lower() and query.lower() not in obj.description.lower():
                match = False
            
            if tags:
                if not any(tag in obj.tags for tag in tags):
                    match = False
                    
            if department and obj.department != department:
                match = False
                
            if role and obj.role != role:
                match = False
                
            if match:
                results.append(obj)
                
        logger.debug(f"Knowledge Search yielded {len(results)} results.")
        return results
