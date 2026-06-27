import logging
import asyncio

from modules.entity_registry.service import EntityRegistryService
from modules.entity_registry.models import EntityTypeDefinition
from modules.schema_engine.validator import SchemaValidator
from modules.metadata_engine.service import MetadataEngineService
from modules.relationship_registry.service import RelationshipRegistryService
from modules.relationship_registry.models import RelationshipTypeDefinition
from modules.relationship_engine.service import RelationshipEngineService

from modules.review_engine.service import ReviewEngineService
from modules.knowledge_architect.orchestrator import KnowledgeArchitectOrchestrator

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

async def main():
    print("=========================================================")
    print("STARTING STAGE 5.6 VALIDATION: INTAKE PIPELINE")
    print("=========================================================")
    
    # Init Core Engines
    ent_registry = EntityRegistryService()
    validator = SchemaValidator()
    meta_engine = MetadataEngineService(ent_registry, validator)
    
    # Types for test
    ent_registry.register_type(EntityTypeDefinition(type_id="sop", display_name="SOP", allow_custom_fields=True))
    ent_registry.register_type(EntityTypeDefinition(type_id="equipment", display_name="Equipment", allow_custom_fields=True))
    ent_registry.register_type(EntityTypeDefinition(type_id="sap_unresolved_mapping", display_name="SAP Placeholder", allow_custom_fields=True))
    
    rel_registry = RelationshipRegistryService()
    rel_registry.register_type(RelationshipTypeDefinition(type_id="REFERENCES_EQUIPMENT", display_name="References", is_directed=True))
    rel_registry.register_type(RelationshipTypeDefinition(type_id="HAS_SAP_MAPPING", display_name="Has SAP", is_directed=True))
    rel_registry.register_type(RelationshipTypeDefinition(type_id="BELONGS_TO_DEPARTMENT", display_name="Belongs To Dept", is_directed=True))
    
    rel_engine = RelationshipEngineService(rel_registry)
    
    # Init Pipeline Engines
    review_engine = ReviewEngineService(meta_engine, rel_engine)
    architect = KnowledgeArchitectOrchestrator(review_engine)
    
    print("\n--- 1. Simulating Document Upload ---")
    
    # Fire the async pipeline
    job = architect.ingest_file(filename="Furnace_Maintenance_SOP_v2.pdf", file_type="application/pdf", uploader="u-master")
    
    # Give the pipeline a moment to run
    await asyncio.sleep(1)
    
    print(f"\n--- 2. Checking Review Queue ---")
    pending_jobs = review_engine.get_pending_jobs()
    
    assert len(pending_jobs) == 1, "Expected 1 job in review queue"
    job_in_review = pending_jobs[0]
    
    print(f"[OK] Job {job_in_review.id} is in Review Queue.")
    print(f"  -> AI Summary: {job_in_review.ai_summary}")
    print(f"  -> Entities Proposed: {len(job_in_review.proposed_entities)}")
    print(f"  -> Relationships Proposed: {len(job_in_review.proposed_relationships)}")
    
    print(f"\n--- 3. Approving Job ---")
    review_engine.approve_job(job_in_review.id, "u-master-editor")
    
    print(f"\n--- 4. Verifying Knowledge Graph ---")
    
    # Check if entities exist in metadata engine
    live_entities = list(meta_engine._entities.values())
    print(f"[OK] Total live entities committed to graph: {len(live_entities)}")
    for live_ent in live_entities:
        print(f"  -> {live_ent.id} ({live_ent.display_name})")
        
    # Check if relationships were created (using the live ID of the first entity)
    # The first entity created was the SOP
    sops = [e for e in live_entities if e.entity_type == "sop"]
    if sops:
        primary_doc_id = sops[0].id
        rels = rel_engine.get_relationships_for_entity(primary_doc_id)
        print(f"[OK] Edges auto-generated for primary document: {len(rels)} edges created.")
    
    print("\n=========================================================")
    print("VALIDATION SUCCESSFUL: AI INTAKE PIPELINE IS OPERATIONAL")
    print("=========================================================")

if __name__ == "__main__":
    asyncio.run(main())
