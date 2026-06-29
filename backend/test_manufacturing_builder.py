import logging
import asyncio

from modules.metadata_engine.repository import MetadataRepository
from modules.entity_registry.models import EntityTypeDefinition
from modules.schema_engine.validator import SchemaValidator
from modules.metadata_engine.service import MetadataEngineService
from modules.relationship_registry.service import RelationshipRegistryService
from modules.relationship_registry.models import RelationshipTypeDefinition
from modules.relationship_engine.service import RelationshipEngineService

from modules.process_modeling.models import ManufacturingFlow, ProcessNode, ProcessEdge, StageConfiguration
from modules.process_runtime.engine import ProcessRuntimeEngine
from modules.manufacturing_builder.service import ManufacturingBuilderService

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

async def main():
    print("=========================================================")
    print("STARTING STAGE 5.5 VALIDATION: MANUFACTURING BUILDER")
    print("=========================================================")
    
    # Init Core Engines
    repo = MetadataRepository()
    validator = SchemaValidator()
    meta_engine = MetadataEngineService(repo, validator)
    
    rel_registry = RelationshipRegistryService()
    rel_registry.register_type(RelationshipTypeDefinition(type_id="NEXT_STAGE", display_name="Next Stage", is_directed=True))
    rel_registry.register_type(RelationshipTypeDefinition(type_id="REQUIRES_SOP", display_name="Requires SOP", is_directed=True))
    rel_registry.register_type(RelationshipTypeDefinition(type_id="USES_EQUIPMENT", display_name="Uses Equipment", is_directed=True))
    rel_engine = RelationshipEngineService(rel_registry)
    
    # Init Builder Engines
    runtime_engine = ProcessRuntimeEngine(meta_engine, rel_engine)
    builder_svc = ManufacturingBuilderService(runtime_engine)
    
    print("\n--- 1. Testing AI Assistance (Draft Flow) ---")
    
    draft_flow = ManufacturingFlow(
        id="flow-test-1",
        name="Steel Refining Flow",
        plant_id="plant-1",
        nodes=[
            ProcessNode(
                id="stage-eaf",
                type="manufacturing_stage",
                label="Electric Arc Furnace",
                configuration=StageConfiguration(estimated_duration_minutes=150)
                # Intentionally missing equipment and SOPs
            ),
            ProcessNode(
                id="stage-aod",
                type="manufacturing_stage",
                label="Argon Oxygen Decarburization",
                equipment_ids=["eq-aod-1"],
                configuration=StageConfiguration(required_sops=["sop-aod-1"])
            )
        ],
        edges=[
            ProcessEdge(id="e1", source_id="stage-eaf", target_id="stage-aod", edge_type="NEXT_STAGE")
        ]
    )
    
    builder_svc.save_flow(draft_flow)
    suggestions = builder_svc.get_ai_suggestions(draft_flow.id)
    
    print(f"[OK] Saved Draft Flow. AI generated {len(suggestions)} suggestions.")
    for s in suggestions:
        print(f"  -> {s['message']}")
        
    print("\n--- 2. Testing Process Runtime (Compile Flow) ---")
    
    # Ensure types exist
    meta_engine.register_type(EntityTypeDefinition(type_id="manufacturing_stage", display_name="Stage", allow_custom_fields=True))
    
    # Publish the flow
    builder_svc.publish_flow(draft_flow.id, "u-master-editor")
    
    print("[OK] Flow published successfully.")
    
    # Verify entities were generated
    eaf_entity = meta_engine.get_entity("stage-eaf")
    print(f"[OK] EAF Entity spawned: {eaf_entity.id} (Type: {eaf_entity.entity_type})")
    
    # Verify relationships were generated
    rels = rel_engine.get_relationships_for_entity("stage-eaf", direction="OUT")
    targets = [r.target_entity_id for r in rels]
    print(f"[OK] Graph Edges auto-generated for EAF. Neighbors: {targets}")
    assert "stage-aod" in targets, "Graph did not properly link EAF to AOD"

    print("\n=========================================================")
    print("VALIDATION SUCCESSFUL: MANUFACTURING BUILDER IS OPERATIONAL")
    print("=========================================================")

if __name__ == "__main__":
    asyncio.run(main())
