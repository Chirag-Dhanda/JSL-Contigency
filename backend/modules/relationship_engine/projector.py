import logging
import asyncio
from typing import Any
from .neo4j_repository import Neo4jRepository
from modules.entity_framework.models import EnterpriseEntity
from .models import EnterpriseRelationship

logger = logging.getLogger("GraphProjector")

class GraphProjectionEngine:
    """
    Listens to metadata/relationship changes and projects them onto Neo4j.
    Maintains graph synchronization asynchronously.
    """
    def __init__(self, neo4j_repo: Neo4jRepository):
        self.repo = neo4j_repo

    def project_entity_async(self, entity: EnterpriseEntity):
        """Fire and forget projection of an EnterpriseEntity into a Neo4j Node."""
        asyncio.create_task(self._project_entity(entity))

    def project_relationship_async(self, rel: EnterpriseRelationship):
        """Fire and forget projection of an EnterpriseRelationship into a Neo4j Edge."""
        asyncio.create_task(self._project_relationship(rel))

    async def _project_entity(self, entity: EnterpriseEntity):
        try:
            # Labels will be the entity type (capitalized for convention) + Entity
            labels = ["Entity", entity.entity_type.capitalize()]
            
            # Map metadata to properties (simple flattened dict for now)
            # Complex nested JSON might require flattening or skipping for graph properties
            properties: dict[str, Any] = {
                "name": entity.name,
                "display_name": entity.display_name,
                "status": entity.status if isinstance(entity.status, str) else entity.status.value,
                "version": entity.version
            }
            
            # Add simple scalars from metadata
            for k, v in entity.metadata.items():
                if isinstance(v, (str, int, float, bool)):
                    properties[k] = v
                    
            await self.repo.upsert_node(entity.id, labels, properties)
        except Exception as e:
            logger.error(f"Sync failed for Entity {entity.id}: {e}")

    async def _project_relationship(self, rel: EnterpriseRelationship):
        try:
            properties = {
                "id": rel.id,
                "created_by": rel.created_by
            }
            properties.update(rel.metadata)
            await self.repo.upsert_relationship(
                source_id=rel.source_entity_id,
                target_id=rel.target_entity_id,
                rel_type=rel.relationship_type.upper(),
                properties=properties
            )
        except Exception as e:
            logger.error(f"Sync failed for Relationship {rel.id}: {e}")
