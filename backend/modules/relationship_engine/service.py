import asyncio
import logging
import inspect
from typing import Dict, Any, List, Optional
from exceptions.base import SystemException, NotFoundException

from .models import EnterpriseRelationship
from .pg_repository import PostgresRelationshipRepository
from .projector import GraphProjectionEngine
from .validator import RelationshipValidator
from modules.relationship_registry.service import RelationshipRegistryService
from modules.metadata_engine.service import MetadataEngineService

logger = logging.getLogger("RelationshipEngine")

def _run(coro):
    """Run a coroutine from sync context safely."""
    try:
        loop = asyncio.get_running_loop()
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(asyncio.run, coro)
            return future.result()
    except RuntimeError:
        return asyncio.run(coro)

class RelationshipEngineService:
    """
    CRUD Engine for creating and managing entity relationships.
    Persists to PostgreSQL and projects to Neo4j automatically.
    """
    
    def __init__(self, 
                 registry: RelationshipRegistryService, 
                 metadata_engine: MetadataEngineService,
                 pg_repo: PostgresRelationshipRepository,
                 projector: GraphProjectionEngine,
                 validator: RelationshipValidator):
        self.registry = registry
        self.metadata_engine = metadata_engine
        self.pg_repo = pg_repo
        self.projector = projector
        self.validator = validator
        logger.info("Relationship Engine Initialized.")

    def _call(self, method_name: str, *args, **kwargs):
        """Dispatch to repository method — handles sync and async transparently."""
        method = getattr(self.pg_repo, method_name)
        result = method(*args, **kwargs)
        if asyncio.iscoroutine(result):
            return _run(result)
        return result

    def create_relationship(self, source_id: str, target_id: str, rel_type: str, created_by: str, metadata: Optional[Dict[str, Any]] = None) -> EnterpriseRelationship:
        """Creates a relationship between two entities."""
        
        # 1. Fetch Types
        try:
            type_def = self.registry.get_type(rel_type)
        except NotFoundException:
            raise SystemException(message=f"Cannot create relationship: Unknown type '{rel_type}'.")
            
        source_entity = self.metadata_engine.get_object(source_id)
        target_entity = self.metadata_engine.get_object(target_id)
        
        source_type_def = self.metadata_engine.get_type(source_entity.entity_type)
        target_type_def = self.metadata_engine.get_type(target_entity.entity_type)

        # 2. Validate
        self.validator.validate_creation(source_type_def, target_type_def, type_def)

        # 3. Create Model
        rel = EnterpriseRelationship(
            source_entity_id=source_id,
            target_entity_id=target_id,
            relationship_type=rel_type,
            direction="DIRECTED" if type_def.is_directed else "BIDIRECTIONAL",
            created_by=created_by,
            metadata=metadata or {}
        )
        
        # 4. Persist to Postgres
        saved_rel = self._call('save_relationship', rel)
        logger.info(f"Created Relationship {rel.id} ({source_id} -[{rel_type}]-> {target_id}) in PG.")
        
        # 5. Project to Neo4j (Async)
        self.projector.project_relationship_async(saved_rel)
        # Ensure nodes exist in Neo4j (just in case they missed sync)
        self.projector.project_entity_async(source_entity)
        self.projector.project_entity_async(target_entity)

        return saved_rel

    def get_relationship(self, rel_id: str) -> EnterpriseRelationship:
        return self._call('get_relationship', rel_id)

    def get_relationships_for_entity(self, entity_id: str, direction: str = "BOTH") -> List[EnterpriseRelationship]:
        """Retrieves all relationships connected to an entity from PostgreSQL."""
        return self._call('get_relationships_for_entity', entity_id, direction)

    def delete_relationship(self, rel_id: str):
        # Fetch first to know what to delete from Neo4j
        try:
            rel = self.get_relationship(rel_id)
            success = self._call('delete_relationship', rel_id)
            if success:
                logger.info(f"Deleted Relationship {rel_id} from PG.")
                
                # Delete from Neo4j (Async wrapper needed in projector)
                # Since projector doesn't have a direct delete_async, we'll dispatch it:
                asyncio.create_task(self.projector.repo.delete_relationship(
                    rel.source_entity_id, 
                    rel.target_entity_id, 
                    rel.relationship_type.upper()
                ))
        except NotFoundException:
            pass
