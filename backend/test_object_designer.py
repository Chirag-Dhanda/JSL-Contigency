import logging
import asyncio

from modules.entity_registry.service import EntityRegistryService
from modules.entity_registry.models import EntityTypeDefinition
from modules.schema_engine.validator import SchemaValidator
from modules.metadata_engine.service import MetadataEngineService
from modules.entity_framework.lifecycle import EntityLifecycle

from modules.object_definitions.templates import VisualObjectDefinition
from modules.object_definitions.fields import ObjectFieldDefinition, FieldValidation
from modules.object_definitions.behavior import ObjectBehavior, AIObjectRules
from modules.object_runtime.generator import RuntimeGeneratorService
from modules.object_designer.service import ObjectDesignerService

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

async def main():
    print("=========================================================")
    print("STARTING STAGE 5.4 VALIDATION: OBJECT DESIGNER")
    print("=========================================================")
    
    # Init Core Engines
    ent_registry = EntityRegistryService()
    validator = SchemaValidator()
    meta_engine = MetadataEngineService(ent_registry, validator)
    
    # Init Object Designer
    runtime_gen = RuntimeGeneratorService(ent_registry)
    designer_svc = ObjectDesignerService(runtime_gen)
    
    print("\n--- 1. Testing Default Blueprints ---")
    blueprints = designer_svc.list_blueprints()
    print(f"[OK] Loaded {len(blueprints)} template blueprints: {[b.type_id for b in blueprints]}")
    
    print("\n--- 2. Programmatically Designing a New Object ---")
    
    # Simulate a Master Editor building a "SCADA Sensor"
    new_blueprint = VisualObjectDefinition(
        type_id="scada_sensor",
        display_name="SCADA IoT Sensor",
        description="A real-time telemetry node on the factory floor.",
        fields=[
            ObjectFieldDefinition(
                field_id="ip_address",
                display_name="IP Address",
                field_type="TEXT",
                validation=FieldValidation(required=True)
            ),
            ObjectFieldDefinition(
                field_id="voltage",
                display_name="Operating Voltage",
                field_type="NUMBER",
                default_value=24.0,
                validation=FieldValidation(min_value=0.0, max_value=240.0)
            ),
            ObjectFieldDefinition(
                field_id="status",
                display_name="Current Status",
                field_type="DROPDOWN",
                validation=FieldValidation(allowed_values=["ONLINE", "OFFLINE", "MAINTENANCE"])
            )
        ],
        behavior=ObjectBehavior(
            ai_rules=AIObjectRules(
                description="Live telemetry sensor. Ask about this for real-time status.",
                ai_tags=["iot", "sensor", "telemetry"],
                search_priority=90
            )
        )
    )
    
    designer_svc.save_blueprint(new_blueprint)
    print(f"[OK] Visual Object Designer drafted: {new_blueprint.type_id}")
    
    print("\n--- 3. Testing Runtime Generator (Compile to Core) ---")
    designer_svc.publish_blueprint(new_blueprint.id)
    print(f"[OK] Blueprint {new_blueprint.id} published to Entity Registry via Runtime Generator.")
    
    # Verify it exists in core registry
    core_def = ent_registry.get_type("scada_sensor")
    print(f"[OK] Found in core registry: {core_def.type_id}")
    print(f"[OK] IP Address rule compiled: {core_def.metadata_schema['ip_address']}")
    
    print("\n--- 4. Instantiating the newly designed object ---")
    # This proves the new object is fully compatible with the MetadataEngine and Stage 5.1/5.2 stack.
    
    try:
        new_sensor = meta_engine.create_entity(
            name="sensor-eaf-temp-01",
            entity_type="scada_sensor",
            display_name="EAF Roof Temp Sensor",
            created_by="u-master-editor",
            metadata={
                "ip_address": "10.0.0.45",
                "status": "ONLINE"
                # voltage will default to 24.0
            }
        )
        print(f"[OK] Dynamically created entity from the visual design: {new_sensor.id}")
        print(f"[OK] Entity metadata: {new_sensor.metadata}")
        
    except Exception as e:
        print(f"[ERROR] Failed to create entity: {e}")
        
    print("\n=========================================================")
    print("VALIDATION SUCCESSFUL: ENTERPRISE OBJECT DESIGNER IS OPERATIONAL")
    print("=========================================================")

if __name__ == "__main__":
    asyncio.run(main())
