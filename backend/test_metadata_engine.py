import logging
import sys

from modules.entity_registry.service import EntityRegistryService
from modules.entity_registry.models import EntityTypeDefinition, ValidationRule
from modules.schema_engine.validator import SchemaValidator
from modules.metadata_engine.service import MetadataEngineService
from modules.entity_framework.lifecycle import EntityLifecycle
from exceptions.base import SystemException

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    print("=========================================================")
    print("STARTING STAGE 5.1 VALIDATION")
    print("=========================================================")
    
    registry = EntityRegistryService()
    validator = SchemaValidator()
    engine = MetadataEngineService(registry, validator)
    
    print("\n--- 1. Registering Dynamic Entity Type ('plc_device') ---")
    plc_def = EntityTypeDefinition(
        type_id="plc_device",
        display_name="PLC Device",
        metadata_schema={
            "voltage": ValidationRule(field_type="number", required=True, min_value=0),
            "manufacturer": ValidationRule(field_type="string", required=True),
            "ip_address": ValidationRule(field_type="string", required=False),
            "protocol": ValidationRule(field_type="string", enum_values=["OPC_UA", "Modbus", "Profinet"])
        },
        default_metadata={"protocol": "OPC_UA"},
        allow_custom_fields=True
    )
    registry.register_type(plc_def)
    print("[OK] Entity Type 'plc_device' registered successfully.")
    
    print("\n--- 2. Creating Valid Entity ---")
    valid_payload = {
        "voltage": 24.5,
        "manufacturer": "Siemens",
        "custom_tag": "Zone-A" # Allowed because allow_custom_fields=True
    }
    
    entity = engine.create_entity(
        name="plc-01",
        entity_type="plc_device",
        display_name="Main Conveyor PLC",
        created_by="system_admin",
        metadata=valid_payload
    )
    print(f"[OK] Entity Created: {entity.id}")
    print(f"   Metadata: {entity.metadata}")
    print(f"   Status: {entity.status.value}")
    
    print("\n--- 3. Testing Schema Validation (Failure Expected) ---")
    invalid_payload = {
        "manufacturer": "Rockwell"
        # Missing required field 'voltage'
    }
    try:
        engine.create_entity("plc-02", "plc_device", "Bad PLC", "admin", invalid_payload)
        print("[FAIL] Schema engine allowed invalid payload.")
        sys.exit(1)
    except SystemException as e:
        print(f"[OK] Expected failure caught by SchemaValidator: {e}")
        
    print("\n--- 4. Updating Metadata ---")
    updated = engine.update_entity_metadata(
        entity_id=entity.id,
        new_metadata={"ip_address": "192.168.1.100"},
        user_id="system_admin"
    )
    print(f"[OK] Metadata updated. New keys: {updated.metadata}")
    print(f"   Version bumped to: {updated.version}")
    
    print("\n--- 5. Lifecycle Transition ---")
    published = engine.transition_lifecycle(entity.id, EntityLifecycle.PUBLISHED)
    print(f"[OK] Entity Status is now: {published.status.value}")
    
    print("\n=========================================================")
    print("VALIDATION SUCCESSFUL: METADATA ENGINE IS OPERATIONAL")
    print("=========================================================")

if __name__ == "__main__":
    main()
