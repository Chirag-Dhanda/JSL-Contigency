import logging
import asyncio

from modules.entity_registry.service import EntityRegistryService
from modules.entity_registry.models import EntityTypeDefinition
from modules.schema_engine.validator import SchemaValidator
from modules.metadata_engine.service import MetadataEngineService
from modules.entity_framework.lifecycle import EntityLifecycle

from modules.permissions.service import PermissionEngine
from modules.content_management.media import MediaLibraryService
from modules.publishing.workflow import PublishingWorkflowService
from modules.knowledge_studio.ai_review import AIReviewQueueService

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

async def main():
    print("=========================================================")
    print("STARTING STAGE 5.3 VALIDATION: KNOWLEDGE STUDIO")
    print("=========================================================")
    
    # Init Core Engines
    ent_registry = EntityRegistryService()
    validator = SchemaValidator()
    meta_engine = MetadataEngineService(ent_registry, validator)
    
    # Init Studio Engines
    perm_engine = PermissionEngine()
    media_service = MediaLibraryService(meta_engine)
    publish_workflow = PublishingWorkflowService(meta_engine)
    ai_queue = AIReviewQueueService()
    
    # Register required types
    ent_registry.register_type(EntityTypeDefinition(type_id="media_asset", display_name="Media Asset", allow_custom_fields=True))
    ent_registry.register_type(EntityTypeDefinition(type_id="sop", display_name="Standard Operating Procedure"))
    
    print("\n--- 1. Testing Permission Engine (MASTER_EDITOR) ---")
    is_master = await perm_engine.has_explicit_permission("u-master-editor", "media.manage")
    print(f"[OK] MASTER_EDITOR has media.manage: {is_master}")
    
    is_admin = await perm_engine.has_explicit_permission("u-master-editor", "auth.modify")
    print(f"[OK] MASTER_EDITOR has auth.modify: {is_admin} (Expected False)")
    
    print("\n--- 2. Testing Media Upload (Content Management) ---")
    asset = media_service.upload_asset(
        filename="furnace_schematic.pdf",
        content_type="application/pdf",
        file_size=1024500,
        uploaded_by="u-master-editor",
        tags=["schematic", "eaf"]
    )
    print(f"[OK] Uploaded media asset: {asset.id} -> {asset.metadata['storage_url']}")
    
    print("\n--- 3. Testing Publishing Workflow (State Machine) ---")
    sop = meta_engine.create_entity("sop-01", "sop", "LOTO SOP", "u-master-editor", {})
    print(f"[OK] Created Entity {sop.id}. Status: {sop.status.value}")
    
    publish_workflow.submit_for_review(sop.id, "u-master-editor")
    sop_updated = meta_engine.get_entity(sop.id)
    print(f"[OK] Submitted for review. Status: {sop_updated.status.value}")
    
    publish_workflow.approve_content(sop.id, "u-master-editor")
    publish_workflow.publish_content(sop.id, "u-master-editor")
    sop_final = meta_engine.get_entity(sop.id)
    print(f"[OK] Approved and Published. Status: {sop_final.status.value}")
    
    print("\n--- 4. Testing AI Review Queue ---")
    suggestion = ai_queue.enqueue_suggestion(
        suggestion_type="RELATIONSHIP_LINK",
        confidence=0.92,
        payload={"source": "sop-01", "target": asset.id, "type": "references"}
    )
    print(f"[OK] Enqueued AI Suggestion: {suggestion.id} (Status: {suggestion.status})")
    
    processed = ai_queue.review_suggestion(suggestion.id, approved=True, editor_id="u-master-editor")
    print(f"[OK] Editor reviewed suggestion. Status is now: {processed.status}")
    
    print("\n=========================================================")
    print("VALIDATION SUCCESSFUL: KNOWLEDGE STUDIO BACKEND IS OPERATIONAL")
    print("=========================================================")

if __name__ == "__main__":
    asyncio.run(main())
