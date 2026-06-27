import logging
import asyncio
from modules.entity_registry.service import EntityRegistryService
from modules.schema_engine.validator import SchemaValidator
from modules.metadata_engine.service import MetadataEngineService
from modules.relationship_registry.service import RelationshipRegistryService
from modules.relationship_registry.models import RelationshipTypeDefinition
from modules.relationship_engine.service import RelationshipEngineService
from modules.review_engine.service import ReviewEngineService
from modules.knowledge_architect.orchestrator import KnowledgeArchitectOrchestrator
from modules.media_platform.service import MediaPlatformService
from modules.media_ai.service import MediaAIIntelligenceService
from modules.thumbnail_engine.service import ThumbnailEngineService

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

async def seed_demo_environment():
    print("=========================================================")
    print("SEEDING MASSIVE ENTERPRISE DEMO ENVIRONMENT (5.5)")
    print("=========================================================")
    
    # Init Core Engines
    ent_registry = EntityRegistryService()
    validator = SchemaValidator()
    meta_engine = MetadataEngineService(ent_registry, validator)
    
    rel_registry = RelationshipRegistryService()
    rel_types = ["BELONGS_TO_PLANT", "BELONGS_TO", "USES_EQUIPMENT", "REQUIRES_SOP", "REQUIRES_LESSON", "NEXT_STAGE", "REFERENCES_EQUIPMENT", "HAS_SAP_MAPPING"]
    for rt in rel_types:
        rel_registry.register_type(RelationshipTypeDefinition(type_id=rt, display_name=rt, is_directed=True))
        
    rel_engine = RelationshipEngineService(rel_registry)
    
    review_engine = ReviewEngineService(meta_engine, rel_engine)
    architect = KnowledgeArchitectOrchestrator(review_engine)
    
    media_engine = MediaPlatformService()
    media_ai = MediaAIIntelligenceService()
    media_thumb = ThumbnailEngineService()
    
    # 1. Create Core Entity Types (simulating Object Designer)
    types = ["plant", "department", "manufacturing_stage", "equipment", "sop", "lesson", "assessment", "safety_doc"]
    for t in types:
        try:
            from modules.entity_registry.models import EntityTypeDefinition
            # Simple allow_custom_fields=True for all types in demo
            ent_registry.register_type(EntityTypeDefinition(type_id=t, display_name=t.replace("_", " ").title(), allow_custom_fields=True))
        except Exception:
            pass
            
    # Keep track of IDs
    plants = []
    departments = []
    equipment = []
    sops = []
    lessons = []
    
    print("\n--- Generating Plants & Departments ---")
    for i in range(1, 4):
        plant = meta_engine.create_entity(f"plant-{i}", "plant", f"Manufacturing Plant 0{i}", "system", {"location": f"Zone {i}"})
        plants.append(plant.id)
        
    for i in range(1, 11):
        dept = meta_engine.create_entity(f"dept-{i}", "department", f"Department {i}", "system", {"headcount": 50})
        departments.append(dept.id)
        # Assign to a random plant
        rel_engine.create_relationship(dept.id, plants[i % 3], "BELONGS_TO_PLANT", "system")
        
    print("\n--- Generating Documents & Assets ---")
    for i in range(1, 85):
        eq = meta_engine.create_entity(f"eq-{i}", "equipment", f"Heavy Machinery {i}", "system", {"status": "ONLINE"})
        equipment.append(eq.id)
        
    for i in range(1, 105):
        sop = meta_engine.create_entity(f"sop-{i}", "sop", f"Standard Operating Procedure {i}", "system", {"version": "v1.2"})
        sops.append(sop.id)
        
    for i in range(1, 105):
        lesson = meta_engine.create_entity(f"lesson-{i}", "lesson", f"Training Module {i}", "system", {"duration": 45})
        lessons.append(lesson.id)
        
    print("\n--- Generating Manufacturing Stages ---")
    for i in range(1, 45):
        stage = meta_engine.create_entity(f"stage-{i}", "manufacturing_stage", f"Process Stage {i}", "system", {"estimated_duration": 120})
        
        # Connect to department
        rel_engine.create_relationship(stage.id, departments[i % 10], "BELONGS_TO", "system")
        
        # Connect to equipment
        rel_engine.create_relationship(stage.id, equipment[i % len(equipment)], "USES_EQUIPMENT", "system")
        rel_engine.create_relationship(stage.id, equipment[(i+1) % len(equipment)], "USES_EQUIPMENT", "system")
        
        # Connect to SOPs
        rel_engine.create_relationship(stage.id, sops[i % len(sops)], "REQUIRES_SOP", "system")
        rel_engine.create_relationship(stage.id, sops[(i+2) % len(sops)], "REQUIRES_SOP", "system")
        
        # Connect to Lessons
        rel_engine.create_relationship(stage.id, lessons[i % len(lessons)], "REQUIRES_LESSON", "system")
        
        # Chain them together
        if i > 1:
            rel_engine.create_relationship(f"stage-{i-1}", stage.id, "NEXT_STAGE", "system")
            
    print(f"\n[OK] Generated {len(plants)} Plants")
    print(f"[OK] Generated {len(departments)} Departments")
    print(f"[OK] Generated {len(equipment)} Equipment Assets")
    print(f"[OK] Generated {len(sops)} SOPs")
    print(f"[OK] Generated {len(lessons)} Lessons")
    print(f"[OK] Generated 44 Manufacturing Stages")
    
    print("\n--- Simulating AI Knowledge Intake ---")
    architect.ingest_file("Scrap_Yard_Safety_Protocol.pdf", "pdf", "system")
    architect.ingest_file("AOD_Furnace_Manual.docx", "docx", "system")
    architect.ingest_file("Rolling_Mill_Maintenance.pdf", "pdf", "system")
    
    await asyncio.sleep(2)
    pending_jobs = review_engine.get_pending_jobs()
    print(f"[OK] Simulated {len(pending_jobs)} pending intake jobs in Review Queue.")
    
    print("\n--- Generating Enterprise Media Library (Stage 5.7) ---")
    media_types = [
        {"ext": ".pdf", "mime": "application/pdf", "prefix": "Manual", "count": 100},
        {"ext": ".jpg", "mime": "image/jpeg", "prefix": "Incident_Photo", "count": 200},
        {"ext": ".mp4", "mime": "video/mp4", "prefix": "Training_Video", "count": 50},
        {"ext": ".dwg", "mime": "application/acad", "prefix": "Engineering_Drawing", "count": 25},
        {"ext": ".docx", "mime": "application/msword", "prefix": "SOP", "count": 100}
    ]
    
    total_media = 0
    for mt in media_types:
        for i in range(mt["count"]):
            filename = f"{mt['prefix']}_{total_media}{mt['ext']}"
            
            # 1. Register Asset
            asset = media_engine.register_asset(
                filename=filename,
                file_type=mt["mime"],
                owner="system",
                file_size=2048 * (i + 1)
            )
            
            # 2. Add AI Keywords (mocked based on random chance or just index)
            if i % 3 == 0:
                asset.filename = f"Safety_{asset.filename}"
            if i % 4 == 0:
                asset.filename = f"EAF_{asset.filename}"
                
            ai_res = media_ai.analyze_asset(asset)
            asset = media_engine.update_metadata(asset.id, tags=ai_res["suggested_tags"], keywords=ai_res["keywords"])
            
            # 3. Gen thumb
            _ = media_thumb.generate_thumbnail(asset)
            
            total_media += 1
            
    print(f"[OK] Generated {total_media} Media Assets with full AI metadata & versioning.")
    
    print("\n=========================================================")
    print("DEMO ENVIRONMENT SEEDED SUCCESSFULLY")
    print("=========================================================")

if __name__ == "__main__":
    asyncio.run(seed_demo_environment())
