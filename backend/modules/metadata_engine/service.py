import logging
from typing import Dict, Any, List, Optional
from core.di import container
from modules.entity_framework.models import EnterpriseEntity
from modules.entity_framework.lifecycle import EntityLifecycle
from modules.schema_engine.validator import SchemaValidator
from modules.entity_registry.models import EntityTypeDefinition
from exceptions.base import SystemException
from .repository import MetadataRepository

logger = logging.getLogger("MetadataEngine")

class MetadataEngineService:
    """
    The master controller for Enterprise Metadata Engine.
    Orchestrates Registry lookups, Schema validation, Versioning, and Data persistence.
    """
    
    def __init__(self, repository: MetadataRepository, validator: SchemaValidator):
        self.repository = repository
        self.validator = validator
        logger.info("Metadata Engine Core Initialized.")

    # ---------------------------------------------------------
    # TYPE / TEMPLATE MANAGEMENT
    # ---------------------------------------------------------
    def register_type(self, type_def: EntityTypeDefinition) -> EntityTypeDefinition:
        """Registers a new Metadata Template (Type)."""
        logger.info(f"Registering metadata type: {type_def.type_id}")
        return self.repository.save_type(type_def)
        
    def update_type(self, type_id: str, updates: dict) -> EntityTypeDefinition:
        """Updates an existing Metadata Template."""
        type_def = self.repository.get_type(type_id)
        # Update logic here (omitted detailed merging for brevity, replacing fields)
        for key, value in updates.items():
            if hasattr(type_def, key):
                setattr(type_def, key, value)
        type_def.version += 1
        return self.repository.save_type(type_def)

    def get_type(self, type_id: str) -> EntityTypeDefinition:
        return self.repository.get_type(type_id)
        
    def list_types(self) -> List[EntityTypeDefinition]:
        return self.repository.list_types()
        
    def delete_type(self, type_id: str) -> bool:
        return self.repository.delete_type(type_id)

    # ---------------------------------------------------------
    # OBJECT MANAGEMENT
    # ---------------------------------------------------------
    def create_object(self, name: str, entity_type: str, display_name: str, created_by: str, metadata: Dict[str, Any]) -> EnterpriseEntity:
        """Creates a new dynamic metadata object."""
        type_def = self.get_type(entity_type)
        
        # Merge Default Metadata
        final_metadata = {**type_def.default_metadata, **metadata}
        
        # Validate Payload
        self.validator.validate(final_metadata, type_def)
        
        # Construct Entity
        entity = EnterpriseEntity(
            name=name,
            entity_type=entity_type,
            display_name=display_name,
            created_by=created_by,
            metadata=final_metadata
        )
        
        # Extension Point: Knowledge Studio Trigger
        self._notify_knowledge_studio(entity)
        
        return self.repository.save_object(entity)

    def get_object(self, object_id: str) -> EnterpriseEntity:
        return self.repository.get_object(object_id)

    def update_object(self, object_id: str, new_metadata: Dict[str, Any], user_id: str) -> EnterpriseEntity:
        """Updates the metadata payload with version tracking."""
        entity = self.get_object(object_id)
        type_def = self.get_type(entity.entity_type)
        
        updated_metadata = {**entity.metadata, **new_metadata}
        self.validator.validate(updated_metadata, type_def)
        
        entity.metadata = updated_metadata
        entity.version += 1
        
        logger.info(f"Updated metadata for Object {object_id} (Version {entity.version}) by {user_id}")
        return self.repository.save_object(entity)

    def search_objects(self, query: str) -> List[EnterpriseEntity]:
        """Search metadata objects."""
        # Extension Point: Semantic Search AI Integration
        return self.repository.search_objects(query)

    def validate_object(self, type_id: str, metadata: Dict[str, Any]) -> bool:
        """Dry-run validation of a metadata payload."""
        type_def = self.get_type(type_id)
        return self.validator.validate(metadata, type_def)

    # ---------------------------------------------------------
    # EXTENSION POINTS
    # ---------------------------------------------------------
    def _notify_knowledge_studio(self, entity: EnterpriseEntity):
        """Extension Point: Notify Knowledge Studio of new objects for indexing."""
        logger.debug(f"Extension Point: Notifying Knowledge Studio for {entity.id}")
        
    def _resolve_relationships(self, entity: EnterpriseEntity):
        """Extension Point: Trigger Relationship Engine."""
        pass
