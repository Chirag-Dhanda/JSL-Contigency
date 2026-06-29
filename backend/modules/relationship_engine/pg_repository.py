import json
import logging
from typing import Dict, Any, List, Optional
from sqlalchemy import select, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import get_async_session
from database.models import DbEnterpriseRelationship
from .models import EnterpriseRelationship
from exceptions.base import NotFoundException

logger = logging.getLogger("RelationshipRepository.PG")

class PostgresRelationshipRepository:
    """Async PostgreSQL persistence for Enterprise Relationships."""

    async def save_relationship(self, rel: EnterpriseRelationship) -> EnterpriseRelationship:
        async with get_async_session() as session:
            existing = await session.get(DbEnterpriseRelationship, rel.id)
            if existing:
                existing.rel_metadata = rel.metadata # type: ignore
                logger.debug(f"Updated relationship: {rel.id}")
            else:
                row = DbEnterpriseRelationship(
                    id=rel.id,
                    source_entity_id=rel.source_entity_id,
                    target_entity_id=rel.target_entity_id,
                    relationship_type=rel.relationship_type,
                    direction=rel.direction,
                    created_by=rel.created_by,
                    rel_metadata=rel.metadata
                )
                session.add(row)
                logger.debug(f"Inserted relationship: {rel.id}")
        return rel

    async def get_relationship(self, rel_id: str) -> EnterpriseRelationship:
        async with get_async_session() as session:
            row = await session.get(DbEnterpriseRelationship, rel_id)
            if not row:
                raise NotFoundException(message=f"Relationship '{rel_id}' not found.")
            return self._row_to_rel(row)

    async def get_relationships_for_entity(self, entity_id: str, direction: str = "BOTH") -> List[EnterpriseRelationship]:
        async with get_async_session() as session:
            stmt = select(DbEnterpriseRelationship)
            
            if direction == "OUT":
                stmt = stmt.where(DbEnterpriseRelationship.source_entity_id == entity_id)
            elif direction == "IN":
                stmt = stmt.where(DbEnterpriseRelationship.target_entity_id == entity_id)
            else:
                stmt = stmt.where(
                    or_(
                        DbEnterpriseRelationship.source_entity_id == entity_id,
                        DbEnterpriseRelationship.target_entity_id == entity_id
                    )
                )
                
            result = await session.execute(stmt)
            rows = result.scalars().all()
            return [self._row_to_rel(r) for r in rows]

    async def delete_relationship(self, rel_id: str) -> bool:
        async with get_async_session() as session:
            row = await session.get(DbEnterpriseRelationship, rel_id)
            if not row:
                return False
            await session.delete(row)
            logger.info(f"Deleted relationship: {rel_id}")
            return True

    def _row_to_rel(self, row: DbEnterpriseRelationship) -> EnterpriseRelationship:
        return EnterpriseRelationship(
            id=row.id, # type: ignore
            source_entity_id=row.source_entity_id, # type: ignore
            target_entity_id=row.target_entity_id, # type: ignore
            relationship_type=row.relationship_type, # type: ignore
            direction=row.direction, # type: ignore
            created_by=row.created_by, # type: ignore
            metadata=row.rel_metadata or {} # type: ignore
        )
