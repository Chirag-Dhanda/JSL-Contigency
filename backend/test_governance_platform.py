import logging
from modules.entity_registry.service import EntityRegistryService
from modules.schema_engine.validator import SchemaValidator
from modules.metadata_engine.service import MetadataEngineService
from modules.entity_registry.models import EntityTypeDefinition
from modules.relationship_registry.service import RelationshipRegistryService
from modules.relationship_registry.models import RelationshipTypeDefinition
from modules.relationship_engine.service import RelationshipEngineService

from modules.governance.models import LifecycleState
from modules.audit_engine.service import AuditEngineService
from modules.version_engine.service import VersionEngineService
from modules.compliance.service import ComplianceEngineService
from modules.publishing_engine.service import PublishingEngineService

logging.basicConfig(level=logging.ERROR)

def main():
    print("=========================================================")
    print("STARTING STAGE 5.10 VALIDATION: GOVERNANCE PLATFORM")
    print("=========================================================")
    
    # 1. Init Base Engines
    ent_registry = EntityRegistryService()
    types = ["plant", "sop"]
    for t in types:
        ent_registry.register_type(EntityTypeDefinition(type_id=t, display_name=t.capitalize(), json_schema={}))
    validator = SchemaValidator()
    meta_engine = MetadataEngineService(ent_registry, validator)
    
    rel_registry = RelationshipRegistryService()
    rel_registry.register_type(RelationshipTypeDefinition(type_id="REQUIRES_SOP", display_name="REQUIRES_SOP", is_directed=True))
    rel_engine = RelationshipEngineService(rel_registry)
    
    # 2. Init Governance Engines
    audit_engine = AuditEngineService()
    version_engine = VersionEngineService(meta_engine)
    compliance_engine = ComplianceEngineService(rel_engine)
    pub_engine = PublishingEngineService(meta_engine, version_engine, audit_engine, compliance_engine)
    
    # 3. Create Entity (Draft)
    p1 = meta_engine.create_entity(name="Jajpur Plant v1", entity_type="plant", display_name="Jajpur Plant", created_by="u-demo", metadata={"location": "Odisha"})
    s1 = meta_engine.create_entity(name="Safety Protocol", entity_type="sop", display_name="Safety Protocol", created_by="u-demo", metadata={})
    rel_engine.create_relationship(p1.id, s1.id, "REQUIRES_SOP", created_by="u-demo")
    
    print(f"\n--- 1. Testing Lifecycle Transitions ---")
    print(f"Initial State: {pub_engine.get_state(p1.id)}")
    
    pub_engine.transition_to_review(p1.id, "u-editor")
    print(f"State after submit: {pub_engine.get_state(p1.id)}")
    
    pub_engine.approve_draft(p1.id, "u-manager")
    print(f"State after approval: {pub_engine.get_state(p1.id)}")
    
    # 4. Publish & Compliance Check
    print(f"\n--- 2. Testing Compliance & Publishing ---")
    pub_engine.publish(p1.id, "u-master_editor", "Initial plant release")
    print(f"Final State: {pub_engine.get_state(p1.id)}")
    
    # 5. Check Versions
    print(f"\n--- 3. Testing Version Engine ---")
    versions = version_engine.get_version_history(p1.id)
    print(f"Version Count: {len(versions)}")
    v1 = versions[0]
    print(f"Version string: v{v1.major_version}.{v1.minor_version}.{v1.patch_version}")
    
    # Update entity for a new version
    p1.name = "Jajpur Plant v2"
    p1.metadata["capacity"] = "1.5 MTPA"
    pub_engine.publish(p1.id, "u-master_editor", "Capacity expansion")
    
    versions = version_engine.get_version_history(p1.id)
    v2 = versions[-1]
    print(f"New Version string: v{v2.major_version}.{v2.minor_version}.{v2.patch_version}")
    print(f"Current Name: {p1.name}")
    
    # 6. Test Rollback
    print(f"\n--- 4. Testing Rollback ---")
    version_engine.rollback(p1.id, v1.id)
    print(f"Name after rollback to v1: {p1.name}")
    assert p1.name == "Jajpur Plant v1", "Rollback failed"
    
    # 7. Check Audits
    print(f"\n--- 5. Testing Audit Ledger ---")
    audits = audit_engine.get_history_for_entity(p1.id)
    print(f"Total Audit Records for {p1.id}: {len(audits)}")
    for a in audits:
        print(f"  [{a.timestamp}] {a.user_id} -> {a.action} ({a.reason or ''})")

    print("\n=========================================================")
    print("VALIDATION SUCCESSFUL: GOVERNANCE PLATFORM IS OPERATIONAL")
    print("=========================================================")

if __name__ == "__main__":
    main()
