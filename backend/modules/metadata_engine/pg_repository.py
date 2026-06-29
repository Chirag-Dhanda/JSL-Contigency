"""
modules/metadata_engine/pg_repository.py
─────────────────────────────────────────────────────────────────
PostgreSQL-backed implementation of MetadataRepository.

Replaces the in-memory dict store with durable async persistence.
Conforms to the same interface as the original MetadataRepository so
no service-layer code requires changes (pure substitution).
"""
from __future__ import annotations

import json
import logging
from typing import Dict, Any, List, Optional

from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_async_session
from database.models import DbEntityTypeDefinition, DbEnterpriseEntity, DbEntityTypeVersion
from modules.entity_registry.models import EntityTypeDefinition, ValidationRule
from modules.entity_framework.models import EnterpriseEntity
from modules.entity_framework.lifecycle import EntityLifecycle
from exceptions.base import NotFoundException, DatabaseException

logger = logging.getLogger("MetadataRepository.PG")


class PostgresMetadataRepository:
    """
    Async PostgreSQL persistence for the Metadata Engine.
    
    All public methods are async coroutines. The MetadataEngineService
    must be updated to await these calls (see service.py).
    
    Design:
      • EntityTypeDefinition  ↔  entity_type_definitions.payload (JSONB)
      • EnterpriseEntity      ↔  enterprise_entities.payload (JSONB)
      • Promoted columns (entity_type, status, created_by, etc.) enable
        efficient filtering without full JSONB scans.
    """

    # ──────────────────────────────────────────────────────────
    # TYPE DEFINITIONS
    # ──────────────────────────────────────────────────────────

    async def save_type(self, type_def: EntityTypeDefinition) -> EntityTypeDefinition:
        async with get_async_session() as session:
            existing = await session.get(DbEntityTypeDefinition, type_def.type_id)
            payload = type_def.model_dump()

            if existing:
                existing.display_name = type_def.display_name
                existing.description = type_def.description
                existing.status = type_def.status
                existing.version = type_def.version
                existing.is_active = type_def.is_active
                existing.payload = payload
                logger.debug(f"Updated entity type: {type_def.type_id}")
            else:
                row = DbEntityTypeDefinition(
                    type_id=type_def.type_id,
                    display_name=type_def.display_name,
                    description=type_def.description,
                    status=type_def.status,
                    version=type_def.version,
                    is_active=type_def.is_active,
                    payload=payload,
                )
                session.add(row)
                logger.debug(f"Inserted entity type: {type_def.type_id}")
        return type_def

    async def get_type(self, type_id: str) -> EntityTypeDefinition:
        async with get_async_session() as session:
            row = await session.get(DbEntityTypeDefinition, type_id)
            if not row:
                raise NotFoundException(message=f"Metadata Type '{type_id}' not found.")
            return self._row_to_type_def(row)

    async def list_types(self) -> List[EntityTypeDefinition]:
        async with get_async_session() as session:
            result = await session.execute(select(DbEntityTypeDefinition))
            rows = result.scalars().all()
            return [self._row_to_type_def(r) for r in rows]

    async def delete_type(self, type_id: str) -> bool:
        async with get_async_session() as session:
            row = await session.get(DbEntityTypeDefinition, type_id)
            if not row:
                return False
            await session.delete(row)
            logger.info(f"Deleted entity type: {type_id}")
        return True

    async def save_type_version(self, type_def: EntityTypeDefinition, user_id: str) -> None:
        """Snapshots the given type definition into the version history table."""
        async with get_async_session() as session:
            payload = type_def.model_dump()
            row = DbEntityTypeVersion(
                type_id=type_def.type_id,
                version=type_def.version,
                status=type_def.status,
                payload=payload,
                created_by=user_id
            )
            session.add(row)
            logger.debug(f"Saved version {type_def.version} for entity type {type_def.type_id}")

    async def get_type_versions(self, type_id: str) -> List[EntityTypeDefinition]:
        """Returns the version history for a given type, ordered from newest to oldest."""
        async with get_async_session() as session:
            stmt = select(DbEntityTypeVersion).where(DbEntityTypeVersion.type_id == type_id).order_by(DbEntityTypeVersion.version.desc())
            result = await session.execute(stmt)
            rows = result.scalars().all()
            return [self._version_row_to_type_def(r) for r in rows]

    async def get_type_version(self, type_id: str, version: int) -> EntityTypeDefinition:
        """Retrieves a specific version of an entity type."""
        async with get_async_session() as session:
            stmt = select(DbEntityTypeVersion).where(
                DbEntityTypeVersion.type_id == type_id,
                DbEntityTypeVersion.version == version
            )
            result = await session.execute(stmt)
            row = result.scalars().first()
            if not row:
                raise NotFoundException(message=f"Version {version} of Metadata Type '{type_id}' not found.")
            return self._version_row_to_type_def(row)

    # ──────────────────────────────────────────────────────────
    # ENTITY OBJECTS
    # ──────────────────────────────────────────────────────────

    async def save_object(self, entity: EnterpriseEntity) -> EnterpriseEntity:
        async with get_async_session() as session:
            existing = await session.get(DbEnterpriseEntity, entity.id)
            payload = json.loads(entity.model_dump_json())

            if existing:
                existing.name = entity.name
                existing.entity_type = entity.entity_type
                existing.display_name = entity.display_name
                existing.status = entity.status.value if hasattr(entity.status, 'value') else str(entity.status)
                existing.version = entity.version
                existing.created_by = entity.created_by
                existing.payload = payload
                logger.debug(f"Updated entity: {entity.id}")
            else:
                row = DbEnterpriseEntity(
                    id=entity.id,
                    name=entity.name,
                    entity_type=entity.entity_type,
                    display_name=entity.display_name,
                    status=entity.status.value if hasattr(entity.status, 'value') else str(entity.status),
                    version=entity.version,
                    created_by=entity.created_by,
                    payload=payload,
                )
                session.add(row)
                logger.debug(f"Inserted entity: {entity.id}")
        return entity

    async def get_object(self, object_id: str) -> EnterpriseEntity:
        async with get_async_session() as session:
            row = await session.get(DbEnterpriseEntity, object_id)
            if not row:
                raise NotFoundException(message=f"Metadata Object '{object_id}' not found.")
            return self._row_to_entity(row)

    async def list_objects(self, type_id: Optional[str] = None, 
                           limit: int = 100, offset: int = 0) -> List[EnterpriseEntity]:
        async with get_async_session() as session:
            stmt = select(DbEnterpriseEntity)
            if type_id:
                stmt = stmt.where(DbEnterpriseEntity.entity_type == type_id)
            stmt = stmt.order_by(DbEnterpriseEntity.modified_at.desc()).limit(limit).offset(offset)
            result = await session.execute(stmt)
            rows = result.scalars().all()
            return [self._row_to_entity(r) for r in rows]

    async def search_objects(self, query: str, limit: int = 50) -> List[EnterpriseEntity]:
        """
        Searches entity name and display_name with a case-insensitive LIKE.
        EP-07 will replace this with full-text + vector search.
        """
        async with get_async_session() as session:
            q = f"%{query.lower()}%"
            stmt = (
                select(DbEnterpriseEntity)
                .where(
                    func.lower(DbEnterpriseEntity.name).like(q) |
                    func.lower(DbEnterpriseEntity.display_name).like(q)
                )
                .limit(limit)
            )
            result = await session.execute(stmt)
            rows = result.scalars().all()
            return [self._row_to_entity(r) for r in rows]

    async def count_objects(self, type_id: Optional[str] = None) -> int:
        async with get_async_session() as session:
            stmt = select(func.count()).select_from(DbEnterpriseEntity)
            if type_id:
                stmt = stmt.where(DbEnterpriseEntity.entity_type == type_id)
            result = await session.execute(stmt)
            return result.scalar_one()

    # ──────────────────────────────────────────────────────────
    # PRIVATE HELPERS
    # ──────────────────────────────────────────────────────────

    def _row_to_type_def(self, row: DbEntityTypeDefinition) -> EntityTypeDefinition:
        payload = row.payload or {}
        # Reconstruct from stored JSONB payload
        return EntityTypeDefinition.model_validate(payload)

    def _version_row_to_type_def(self, row: DbEntityTypeVersion) -> EntityTypeDefinition:
        payload = row.payload or {}
        return EntityTypeDefinition.model_validate(payload)

    def _row_to_entity(self, row: DbEnterpriseEntity) -> EnterpriseEntity:
        payload = row.payload or {}
        return EnterpriseEntity.model_validate(payload)
