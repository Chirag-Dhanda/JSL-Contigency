import logging
from typing import Dict, Any, List
from modules.metadata_engine.service import MetadataEngineService
from modules.relationship_engine.service import RelationshipEngineService

logger = logging.getLogger("DiscoveryEngine")

class DiscoveryEngineService:
    """
    Centralized Discovery Engine to build Smart Entity Profiles.
    """
    def __init__(self, meta_engine: MetadataEngineService, rel_engine: RelationshipEngineService):
        self.meta_engine = meta_engine
        self.rel_engine = rel_engine
        logger.info("Discovery Engine Initialized.")

    def get_discovery_profile(self, entity_id: str) -> Dict[str, Any]:
        """
        Builds a comprehensive profile for an entity, including its metadata,
        breadcrumbs, and all related objects grouped by relationship type.
        """
        logger.info(f"Building Discovery Profile for: {entity_id}")
        
        entity = self.meta_engine.get_entity(entity_id)
        
        # Get immediate relationships (1 degree of separation)
        rels = self.rel_engine.get_relationships_for_entity(entity_id)
        
        related_objects = {
            "parents": [], # BELONGS_TO, NEXT_STAGE (incoming)
            "children": [], # BELONGS_TO (outgoing), NEXT_STAGE (outgoing)
            "equipment": [], # USES_EQUIPMENT
            "sops": [], # REQUIRES_SOP
            "lessons": [], # REQUIRES_LESSON
            "media": [], # HAS_MEDIA
            "other": []
        }
        
        for rel in rels:
            is_source = rel.source_entity_id == entity_id
            other_id = rel.target_entity_id if is_source else rel.source_entity_id
            
            try:
                other_node = self.meta_engine.get_entity(other_id)
            except:
                continue
                
            rel_type = rel.relationship_type
            
            obj = {
                "id": other_node.id,
                "name": other_node.name,
                "type": other_node.entity_type,
                "relationship": rel_type,
                "direction": "outgoing" if is_source else "incoming"
            }
            
            if rel_type == "BELONGS_TO":
                if is_source:
                    related_objects["parents"].append(obj)
                else:
                    related_objects["children"].append(obj)
            elif rel_type == "NEXT_STAGE":
                if is_source:
                    related_objects["children"].append(obj)
                else:
                    related_objects["parents"].append(obj)
            elif rel_type == "USES_EQUIPMENT":
                related_objects["equipment"].append(obj)
            elif rel_type == "REQUIRES_SOP":
                related_objects["sops"].append(obj)
            elif rel_type == "REQUIRES_LESSON":
                related_objects["lessons"].append(obj)
            elif rel_type == "HAS_MEDIA":
                related_objects["media"].append(obj)
            else:
                related_objects["other"].append(obj)
                
        # Generate Breadcrumbs (traverse parents)
        breadcrumbs = self._generate_breadcrumbs(entity_id)
        
        # Calculate Recommendations (Mock)
        # In reality, this would traverse 2-3 degrees or use collaborative filtering
        recommendations = [
            {"id": "rec-1", "name": f"Suggested Workflow for {entity.name}", "type": "workflow"},
            {"id": "rec-2", "name": f"Recently viewed {entity.entity_type}s", "type": entity.entity_type}
        ]
        
        return {
            "entity": {
                "id": entity.id,
                "name": entity.name,
                "type": entity.entity_type,
                "attributes": entity.metadata
            },
            "breadcrumbs": breadcrumbs,
            "related_objects": related_objects,
            "recommendations": recommendations
        }
        
    def _generate_breadcrumbs(self, entity_id: str) -> List[Dict[str, str]]:
        breadcrumbs = []
        current_id = entity_id
        visited = set()
        
        while current_id and current_id not in visited:
            visited.add(current_id)
            try:
                entity = self.meta_engine.get_entity(current_id)
                breadcrumbs.insert(0, {"id": entity.id, "name": entity.name})
                
                # Find parent (BELONGS_TO)
                rels = self.rel_engine.get_relationships_for_entity(current_id)
                parent_rel = next((r for r in rels if r.source_entity_id == current_id and r.relationship_type == "BELONGS_TO"), None)
                
                if parent_rel:
                    current_id = parent_rel.target_entity_id
                else:
                    current_id = None
            except Exception:
                break
                
        # Always prepend Home
        breadcrumbs.insert(0, {"id": "home", "name": "Enterprise Home"})
        return breadcrumbs
