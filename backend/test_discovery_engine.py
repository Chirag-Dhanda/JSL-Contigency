import logging
import json
from modules.metadata_engine.service import MetadataEngineService
from modules.relationship_engine.service import RelationshipEngineService
from modules.discovery_engine.service import DiscoveryEngineService
from modules.hyperlink_engine.service import HyperlinkEngineService

logging.basicConfig(level=logging.ERROR)

def main():
    print("=========================================================")
    print("STARTING STAGE 5.8 VALIDATION: DISCOVERY ENGINE")
    print("=========================================================")
    
    # 1. Run seeder to get a massive populated environment
    print("\n[INFO] Initializing massive graph from seeder...")
    from modules.entity_registry.service import EntityRegistryService
    from modules.schema_engine.validator import SchemaValidator
    from modules.entity_registry.models import EntityTypeDefinition
    from modules.relationship_registry.service import RelationshipRegistryService
    from modules.relationship_registry.models import RelationshipTypeDefinition
    
    ent_registry = EntityRegistryService()
    types = ["plant", "department", "manufacturing_stage", "equipment", "sop", "lesson", "assessment", "safety_doc"]
    for t in types:
        ent_registry.register_type(EntityTypeDefinition(type_id=t, display_name=t.capitalize(), json_schema={}))
        
    validator = SchemaValidator()
    meta_engine = MetadataEngineService(ent_registry, validator)
    
    rel_registry = RelationshipRegistryService()
    rel_types = ["BELONGS_TO", "USES_EQUIPMENT", "REQUIRES_SOP", "REQUIRES_LESSON", "REQUIRES_EQUIPMENT"]
    for rt in rel_types:
        rel_registry.register_type(RelationshipTypeDefinition(type_id=rt, display_name=rt, is_directed=True))
    rel_engine = RelationshipEngineService(rel_registry)
    
    # We will manually inject a few test nodes to guarantee predictable structure for testing
    p1 = meta_engine.create_entity(name="Jajpur Plant", entity_type="plant", display_name="Jajpur Plant", created_by="system", metadata={"name": "Jajpur Plant"})
    d1 = meta_engine.create_entity(name="Melting Shop", entity_type="department", display_name="Melting Shop", created_by="system", metadata={"name": "Melting Shop"})
    e1 = meta_engine.create_entity(name="Electric Arc Furnace A", entity_type="equipment", display_name="Electric Arc Furnace A", created_by="system", metadata={"name": "Electric Arc Furnace A"})
    s1 = meta_engine.create_entity(name="EAF High Voltage Protocol", entity_type="sop", display_name="EAF High Voltage Protocol", created_by="system", metadata={"name": "EAF High Voltage Protocol"})
    
    rel_engine.create_relationship(d1.id, p1.id, "BELONGS_TO", created_by="system")
    rel_engine.create_relationship(e1.id, d1.id, "BELONGS_TO", created_by="system")
    rel_engine.create_relationship(s1.id, e1.id, "REQUIRES_EQUIPMENT", created_by="system") 
    rel_engine.create_relationship(e1.id, s1.id, "REQUIRES_SOP", created_by="system")
    
    # 2. Init Discovery Engine
    discovery_engine = DiscoveryEngineService(meta_engine, rel_engine)
    
    print("\n--- 1. Testing Smart Entity Profile & Breadcrumbs ---")
    profile = discovery_engine.get_discovery_profile(e1.id)
    
    print(f"\nProfile for: {profile['entity']['name']}")
    print(f"Breadcrumbs: {' > '.join(b['name'] for b in profile['breadcrumbs'])}")
    
    parents = [x['name'] for x in profile['related_objects']['parents']]
    sops = [x['name'] for x in profile['related_objects']['sops']]
    
    print(f"Parents (BELONGS_TO): {parents}")
    print(f"Required SOPs: {sops}")
    
    assert len(profile['breadcrumbs']) == 4, "Expected 4 breadcrumbs: Home > Plant > Dept > Eq"
    assert "Melting Shop" in parents, "Expected Melting Shop as parent"
    assert "EAF High Voltage Protocol" in sops, "Expected SOP in relations"
    print("[OK] Discovery Profile Generated Successfully.")

    print("\n--- 2. Testing Universal Hyperlink Engine ---")
    hyperlink_engine = HyperlinkEngineService(meta_engine)
    
    ai_response = "Before starting the Electric Arc Furnace A, please ensure you review the EAF High Voltage Protocol."
    linked_response = hyperlink_engine.inject_hyperlinks(ai_response)
    
    print(f"\nOriginal AI Response:\n{ai_response}")
    print(f"\nHyperlinked Response:\n{linked_response}")
    
    assert "](/studio/explore/" in linked_response, "Expected markdown links to be injected."
    print("[OK] Hyperlinks Injected Successfully.")

    print("\n=========================================================")
    print("VALIDATION SUCCESSFUL: DISCOVERY ENGINE IS OPERATIONAL")
    print("=========================================================")

if __name__ == "__main__":
    main()
