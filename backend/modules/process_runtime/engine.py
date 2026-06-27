import logging
from typing import Dict, List, Any
from modules.process_modeling.models import ManufacturingFlow
from modules.metadata_engine.service import MetadataEngineService
from modules.relationship_engine.service import RelationshipEngineService

logger = logging.getLogger("ProcessRuntimeEngine")

class ProcessRuntimeEngine:
    """
    Translates visual Manufacturing Flows into actual Enterprise Entities
    and directional Knowledge Graph edges.
    """
    
    def __init__(self, metadata_engine: MetadataEngineService, relationship_engine: RelationshipEngineService):
        self.metadata = metadata_engine
        self.relationships = relationship_engine
        logger.info("Process Runtime Engine Initialized.")
        
    def publish_flow(self, flow: ManufacturingFlow, user_id: str) -> bool:
        """
        Compiles the visual nodes and edges into the graph.
        """
        if not flow.nodes:
            logger.warning(f"Flow {flow.name} has no nodes. Aborting publish.")
            return False
            
        logger.info(f"Publishing Flow: {flow.name} (Nodes: {len(flow.nodes)}, Edges: {len(flow.edges)})")
        
        node_to_entity_map = {}
        
        # 1. Create or Update Entities for each Node
        for node in flow.nodes:
            try:
                # In a real system, we'd check if the entity already exists and update it.
                # For this stage, we assume they are new stages being created.
                
                metadata_payload = {
                    "duration_minutes": node.configuration.estimated_duration_minutes,
                    "required_ppe": node.configuration.required_ppe,
                    "quality_checks": node.configuration.quality_checks,
                    "plant_id": flow.plant_id
                }
                
                # We use a generic 'manufacturing_stage' type if it doesn't map exactly
                entity_type = node.type if node.type in ["manufacturing_stage", "quality_gate", "department"] else "manufacturing_stage"
                
                entity = self.metadata.create_entity(
                    name=node.id,
                    entity_type=entity_type,
                    display_name=node.label,
                    created_by=user_id,
                    metadata=metadata_payload
                )
                node_to_entity_map[node.id] = entity.id
                logger.debug(f"Spawned Entity {entity.id} for node {node.id}")
                
                # Auto-generate intrinsic relationships from node configuration
                if node.department_id:
                    self.relationships.create_relationship(entity.id, node.department_id, "BELONGS_TO", "system")
                    
                for eq_id in node.equipment_ids:
                    self.relationships.create_relationship(entity.id, eq_id, "USES_EQUIPMENT", "system")
                    
                for sop_id in node.configuration.required_sops:
                    self.relationships.create_relationship(entity.id, sop_id, "REQUIRES_SOP", "system")
                    
                for lesson_id in node.configuration.required_lessons:
                    self.relationships.create_relationship(entity.id, lesson_id, "REQUIRES_LESSON", "system")
                    
            except Exception as e:
                logger.error(f"Failed to process node {node.id}: {e}")
                
        # 2. Establish Flow Edges
        for edge in flow.edges:
            source_entity_id = node_to_entity_map.get(edge.source_id)
            target_entity_id = node_to_entity_map.get(edge.target_id)
            
            if source_entity_id and target_entity_id:
                # Add directional relationship in the graph
                self.relationships.create_relationship(
                    source_id=source_entity_id,
                    target_id=target_entity_id,
                    rel_type=edge.edge_type,
                    created_by="system",
                    metadata={"visual_edge_id": edge.id, "label": edge.label}
                )
                logger.debug(f"Connected {source_entity_id} -> {target_entity_id} ({edge.edge_type})")
                
        flow.is_published = True
        logger.info(f"Successfully compiled Flow {flow.name} into the Knowledge Graph.")
        return True
