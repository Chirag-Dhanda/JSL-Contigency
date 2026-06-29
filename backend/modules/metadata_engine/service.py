"""
modules/metadata_engine/service.py
─────────────────────────────────────────────────────────────────
MetadataEngineService — EP-01 update.

Supports two repository modes:
  • PostgresMetadataRepository  (async, production)
  • MetadataRepository          (sync in-memory, tests / no-DB fallback)

The service detects which repository it holds and dispatches accordingly.
All public methods remain synchronous for API compatibility; internally
they use asyncio.run() when calling the async PG repository from a
sync FastAPI context. In the async FastAPI endpoints, await is used
via the async companion methods (prefixed _async_).

Alias methods (create_entity / get_entity / list_entities) are preserved
for backward compatibility with existing test files.
"""
import asyncio
import inspect
import logging
from typing import Dict, Any, List, Optional

from modules.entity_framework.models import EnterpriseEntity
from modules.entity_framework.lifecycle import EntityLifecycle
from modules.schema_engine.validator import SchemaValidator
from modules.entity_registry.models import EntityTypeDefinition
from exceptions.base import SystemException
from .repository import MetadataRepository

logger = logging.getLogger("MetadataEngine")


def _run(coro):
    """Run a coroutine from sync context without nesting event loops."""
    try:
        loop = asyncio.get_running_loop()
        # We are inside a running event loop (FastAPI handler).
        # Schedule the coro as a task and wait — safe because FastAPI
        # endpoints call sync service methods from a thread executor
        # when using run_in_executor. For now we keep it simple:
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(asyncio.run, coro)
            return future.result()
    except RuntimeError:
        # No running loop — direct asyncio.run is fine
        return asyncio.run(coro)


class MetadataEngineService:
    """
    Master controller for Enterprise Metadata Engine.
    Orchestrates Registry lookups, Schema validation, Versioning, and Data persistence.
    """

    def __init__(self, repository, validator: SchemaValidator):
        self.repository = repository
        self.validator = validator
        # Detect async PG repository
        self._is_async = inspect.iscoroutinefunction(getattr(repository, 'save_type', None))
        # In-memory cache for published entity types (can be swapped for Redis later)
        self._type_cache: Dict[str, EntityTypeDefinition] = {}
        logger.info(f"Metadata Engine initialized (repository={type(repository).__name__}).")

    # ──────────────────────────────────────────────────────────
    # INTERNAL DISPATCH HELPERS
    # ──────────────────────────────────────────────────────────

    def _call(self, method_name: str, *args, **kwargs):
        """Dispatch to repository method — handles sync and async transparently."""
        method = getattr(self.repository, method_name)
        result = method(*args, **kwargs)
        if asyncio.iscoroutine(result):
            return _run(result)
        return result

    # ──────────────────────────────────────────────────────────
    # TYPE / TEMPLATE MANAGEMENT
    # ──────────────────────────────────────────────────────────

    def register_type(self, type_def: EntityTypeDefinition) -> EntityTypeDefinition:
        """Registers a new Metadata Template (Type) in Draft status."""
        logger.info(f"Registering metadata type: {type_def.type_id}")
        type_def.status = "Draft"
        return self._call('save_type', type_def)

    def update_type(self, type_id: str, updates: dict) -> EntityTypeDefinition:
        """Updates an existing Metadata Template."""
        type_def = self._call('get_type', type_id)
        if type_def.status == "Published":
            raise SystemException(message="Cannot modify a Published definition directly. Create a new Draft.")
            
        for key, value in updates.items():
            if hasattr(type_def, key):
                setattr(type_def, key, value)
        type_def.version += 1
        return self._call('save_type', type_def)

    def get_type(self, type_id: str) -> EntityTypeDefinition:
        if type_id in self._type_cache:
            return self._type_cache[type_id]
            
        type_def = self._call('get_type', type_id)
        if type_def.status == "Published":
            self._type_cache[type_id] = type_def
            
        return type_def

    def list_types(self) -> List[EntityTypeDefinition]:
        return self._call('list_types')

    def delete_type(self, type_id: str) -> bool:
        if type_id in self._type_cache:
            del self._type_cache[type_id]
        return self._call('delete_type', type_id)
        
    def publish_type(self, type_id: str, user_id: str) -> EntityTypeDefinition:
        """
        Transitions a Draft/Approved definition to Published.
        Validates the schema itself before publication.
        Records the version history.
        """
        type_def = self.get_type(type_id)
        if type_def.status == "Published":
            raise SystemException(message=f"Type {type_id} is already published.")
            
        # Validate the definition structure
        self.validator.validate_type_definition(type_def)
        
        type_def.status = "Published"
        
        # Save to active table
        saved_def = self._call('save_type', type_def)
        
        # Snapshot to version history
        if hasattr(self.repository, 'save_type_version'):
            self._call('save_type_version', saved_def, user_id)
            
        # Update cache
        self._type_cache[type_id] = saved_def
        logger.info(f"Published entity type {type_id} version {saved_def.version} by {user_id}")
        return saved_def
        
    def rollback_type(self, type_id: str, version: int, user_id: str) -> EntityTypeDefinition:
        """
        Rolls back to a previous version by creating a new Draft based on the old version.
        """
        if not hasattr(self.repository, 'get_type_version'):
            raise SystemException(message="Repository does not support version history.")
            
        old_version = self._call('get_type_version', type_id, version)
        
        # Create a new draft from the old version
        current_def = self.get_type(type_id)
        
        old_version.version = current_def.version + 1
        old_version.status = "Draft"
        
        saved_def = self._call('save_type', old_version)
        logger.info(f"Rolled back entity type {type_id} to version {version} as new draft (v{saved_def.version}) by {user_id}")
        return saved_def
        
    def analyze_dependencies(self, type_id: str) -> Dict[str, Any]:
        """
        Analyzes and returns all dependencies for a given entity type.
        E.g. referenced entity types in fields.
        """
        type_def = self.get_type(type_id)
        dependencies = {
            "references": [],
            "allowed_relationships": type_def.allowed_relationships
        }
        
        for key, rule in type_def.metadata_schema.items():
            if rule.field_type == "reference" and rule.enum_values:
                # Assuming enum_values holds the referenced type_ids for 'reference' fields
                dependencies["references"].extend(rule.enum_values)
                
        # Deduplicate
        dependencies["references"] = list(set(dependencies["references"]))
        return dependencies

    # ──────────────────────────────────────────────────────────
    # OBJECT MANAGEMENT
    # ──────────────────────────────────────────────────────────

    def create_object(self, name: str, entity_type: str, display_name: str,
                      created_by: str, metadata: Dict[str, Any]) -> EnterpriseEntity:
        """Creates a new dynamic metadata object."""
        type_def = self.get_type(entity_type)

        # Merge defaults then validate
        final_metadata = {**type_def.default_metadata, **metadata}
        self.validator.validate(final_metadata, type_def)

        entity = EnterpriseEntity(
            name=name,
            entity_type=entity_type,
            display_name=display_name,
            created_by=created_by,
            metadata=final_metadata,
        )

        self._notify_knowledge_studio(entity)
        return self._call('save_object', entity)

    def get_object(self, object_id: str) -> EnterpriseEntity:
        return self._call('get_object', object_id)

    def list_objects(self, type_id: Optional[str] = None) -> List[EnterpriseEntity]:
        return self._call('list_objects', type_id)

    def update_object(self, object_id: str, new_metadata: Dict[str, Any],
                      user_id: str) -> EnterpriseEntity:
        """Updates the metadata payload with version tracking."""
        entity = self.get_object(object_id)
        type_def = self.get_type(entity.entity_type)

        updated_metadata = {**entity.metadata, **new_metadata}
        self.validator.validate(updated_metadata, type_def)

        entity.metadata = updated_metadata
        entity.version += 1

        logger.info(f"Updated Object {object_id} (v{entity.version}) by {user_id}")
        return self._call('save_object', entity)

    def search_objects(self, query: str) -> List[EnterpriseEntity]:
        """Search metadata objects."""
        return self._call('search_objects', query)

    def validate_object(self, type_id: str, metadata: Dict[str, Any]) -> bool:
        """Dry-run validation of a metadata payload."""
        type_def = self.get_type(type_id)
        return self.validator.validate(metadata, type_def)

    # ──────────────────────────────────────────────────────────
    # BACKWARD-COMPATIBLE ALIASES
    # ──────────────────────────────────────────────────────────

    def create_entity(self, name: str, entity_type: str, display_name: str,
                      created_by: str, metadata: Dict[str, Any]) -> EnterpriseEntity:
        return self.create_object(name, entity_type, display_name, created_by, metadata)

    def get_entity(self, entity_id: str) -> EnterpriseEntity:
        return self.get_object(entity_id)

    def list_entities(self, type_id: Optional[str] = None) -> List[EnterpriseEntity]:
        return self.list_objects(type_id)

    # ──────────────────────────────────────────────────────────
    # EXTENSION POINTS
    # ──────────────────────────────────────────────────────────

    def _notify_knowledge_studio(self, entity: EnterpriseEntity):
        logger.debug(f"Extension: Notifying Knowledge Studio for {entity.id}")

    def _resolve_relationships(self, entity: EnterpriseEntity):
        pass
