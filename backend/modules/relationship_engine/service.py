import logging
from typing import Dict, Any, List
from .models import EnterpriseRelationship
from modules.relationship_registry.service import RelationshipRegistryService
from exceptions.base import SystemException, NotFoundException

logger = logging.getLogger("RelationshipEngine")

class RelationshipEngineService:
    """
    CRUD Engine for creating and managing entity relationships.
    """
    
    def __init__(self, registry: RelationshipRegistryService):
        self.registry = registry
        # Mock database for relationships
        self._relationships: Dict[str, EnterpriseRelationship] = {}
        logger.info("Relationship Engine Initialized.")

    def create_relationship(self, source_id: str, target_id: str, rel_type: str, created_by: str, metadata: Dict[str, Any] = None) -> EnterpriseRelationship:
        """Creates a relationship between two entities."""
        # 1. Validate Type
        try:
            type_def = self.registry.get_type(rel_type)
        except NotFoundException:
            raise SystemException(message=f"Cannot create relationship: Unknown type '{rel_type}'.")
            
        # Note: In a full implementation, we would also fetch the Source and Target entities 
        # from the MetadataEngine to validate their `entity_type` against `allowed_source_types`.
            
        rel = EnterpriseRelationship(
            source_entity_id=source_id,
            target_entity_id=target_id,
            relationship_type=rel_type,
            direction="DIRECTED" if type_def.is_directed else "BIDIRECTIONAL",
            created_by=created_by,
            metadata=metadata or {}
        )
        
        self._relationships[rel.id] = rel
        logger.info(f"Created Relationship {rel.id} ({source_id} -[{rel_type}]-> {target_id})")
        return rel

    def get_relationship(self, rel_id: str) -> EnterpriseRelationship:
        if rel_id not in self._relationships:
            raise NotFoundException(message=f"Relationship {rel_id} not found.")
        return self._relationships[rel_id]

    def get_relationships_for_entity(self, entity_id: str, direction: str = "BOTH") -> List[EnterpriseRelationship]:
        """Retrieves all relationships connected to an entity."""
        results = []
        for rel in self._relationships.values():
            if direction in ["OUT", "BOTH"] and rel.source_entity_id == entity_id:
                results.append(rel)
            elif direction in ["IN", "BOTH"] and rel.target_entity_id == entity_id:
                results.append(rel)
            # Handle bidirectional traversal
            elif rel.direction == "BIDIRECTIONAL" and (rel.source_entity_id == entity_id or rel.target_entity_id == entity_id):
                results.append(rel)
        return results

    def delete_relationship(self, rel_id: str):
        if rel_id in self._relationships:
            del self._relationships[rel_id]
            logger.info(f"Deleted Relationship {rel_id}")
