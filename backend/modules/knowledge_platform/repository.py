"""
modules/knowledge_platform/repository.py
────────────────────────────────────────────────────────────────
EP-05: Async PostgreSQL persistence for Knowledge Platform.

Implements all CRUD operations for:
  • KnowledgeAsset
  • KnowledgeChunk (including pgvector semantic_search)
  • IngestionJob
  • OntologyCandidate
  • RelationshipCandidate
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import select, or_, update, text
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_async_session
from database.models import (
    DbKnowledgeAsset, DbKnowledgeChunk, DbIngestionJob,
    DbOntologyCandidate, DbRelationshipCandidate
)
from exceptions.base import NotFoundException
from .models import (
    KnowledgeAsset, KnowledgeChunk, IngestionJob,
    OntologyCandidate, RelationshipCandidate,
    AssetStatus, IngestionStatus, CandidateStatus, ChunkStrategy, StageLogEntry
)

logger = logging.getLogger("KnowledgePlatform.Repository")


class KnowledgeRepository:
    """Async PostgreSQL repository for Knowledge Platform."""

    # ─── KnowledgeAsset ───────────────────────────────────────

    async def save_asset(self, asset: KnowledgeAsset) -> KnowledgeAsset:
        async with get_async_session() as session:
            row = await session.get(DbKnowledgeAsset, asset.id)
            if row:
                row.title = asset.title # type: ignore
                row.status = asset.status.value # type: ignore
                row.updated_at = datetime.now(timezone.utc) # type: ignore
                row.extracted_metadata = asset.extracted_metadata # type: ignore
                row.ontology_tags = asset.ontology_tags # type: ignore
                row.acl = asset.acl # type: ignore
                if asset.published_at:
                    row.published_at = asset.published_at # type: ignore
                if asset.archived_at:
                    row.archived_at = asset.archived_at # type: ignore
            else:
                row = DbKnowledgeAsset(
                    id=asset.id,
                    title=asset.title,
                    asset_type=asset.asset_type,
                    source_filename=asset.source_filename,
                    source_uri=asset.source_uri,
                    status=asset.status.value,
                    version=asset.version,
                    language=asset.language,
                    entity_type_ref=asset.entity_type_ref,
                    department_owner=asset.department_owner,
                    created_by=asset.created_by,
                    extracted_metadata=asset.extracted_metadata,
                    ontology_tags=asset.ontology_tags,
                    acl=asset.acl,
                )
                session.add(row)
        return asset

    async def get_asset(self, asset_id: str) -> KnowledgeAsset:
        async with get_async_session() as session:
            row = await session.get(DbKnowledgeAsset, asset_id)
            if not row:
                raise NotFoundException(message=f"Knowledge asset '{asset_id}' not found.")
            return self._row_to_asset(row)

    async def list_assets(self, status: Optional[str] = None, asset_type: Optional[str] = None,
                          limit: int = 50, offset: int = 0) -> List[KnowledgeAsset]:
        async with get_async_session() as session:
            stmt = select(DbKnowledgeAsset)
            if status:
                stmt = stmt.where(DbKnowledgeAsset.status == status)
            if asset_type:
                stmt = stmt.where(DbKnowledgeAsset.asset_type == asset_type)
            stmt = stmt.order_by(DbKnowledgeAsset.created_at.desc()).limit(limit).offset(offset)
            result = await session.execute(stmt)
            return [self._row_to_asset(r) for r in result.scalars().all()]

    # ─── KnowledgeChunk ───────────────────────────────────────

    async def save_chunks(self, chunks: List[KnowledgeChunk]) -> List[KnowledgeChunk]:
        async with get_async_session() as session:
            for chunk in chunks:
                row = DbKnowledgeChunk(
                    id=chunk.id,
                    asset_id=chunk.asset_id,
                    chunk_index=chunk.chunk_index,
                    chunk_strategy=chunk.chunk_strategy.value,
                    text=chunk.text,
                    char_start=chunk.char_start,
                    char_end=chunk.char_end,
                    token_count=chunk.token_count,
                    chunk_metadata=chunk.chunk_metadata,
                    embedding=chunk.embedding,   # pgvector handles List[float] natively
                    embedding_model=chunk.embedding_model,
                    embedding_version=chunk.embedding_version,
                )
                session.add(row)
        return chunks

    async def update_chunk_embedding(self, chunk_id: str, embedding: List[float],
                                     model: str, version: int) -> None:
        async with get_async_session() as session:
            stmt = (
                update(DbKnowledgeChunk)
                .where(DbKnowledgeChunk.id == chunk_id)
                .values(embedding=embedding, embedding_model=model, embedding_version=version)
            )
            await session.execute(stmt)

    async def get_chunks_for_asset(self, asset_id: str) -> List[KnowledgeChunk]:
        async with get_async_session() as session:
            stmt = (select(DbKnowledgeChunk)
                    .where(DbKnowledgeChunk.asset_id == asset_id)
                    .order_by(DbKnowledgeChunk.chunk_index))
            result = await session.execute(stmt)
            return [self._row_to_chunk(r) for r in result.scalars().all()]

    async def semantic_search(self, embedding: List[float], top_k: int = 5,
                               asset_status_filter: str = "PUBLISHED") -> List[Dict[str, Any]]:
        """
        Executes a pgvector cosine similarity search.
        Returns top_k chunks sorted by proximity to the query embedding.
        """
        async with get_async_session() as session:
            # Convert embedding list to string format pgvector expects
            vec_str = "[" + ",".join(str(v) for v in embedding) + "]"
            sql = text("""
                SELECT
                    kc.id, kc.asset_id, kc.chunk_index, kc.text,
                    kc.embedding <=> :vec AS distance,
                    ka.title AS asset_title,
                    ka.asset_type, ka.source_filename, ka.version
                FROM knowledge_chunks kc
                JOIN knowledge_assets ka ON ka.id = kc.asset_id
                WHERE ka.status = :status
                  AND kc.embedding IS NOT NULL
                ORDER BY distance ASC
                LIMIT :top_k
            """)
            result = await session.execute(sql, {"vec": vec_str, "status": asset_status_filter, "top_k": top_k})
            rows = result.mappings().all()
            return [dict(r) for r in rows]

    async def lexical_search(self, query: str, top_k: int = 5,
                              asset_status_filter: str = "PUBLISHED") -> List[Dict[str, Any]]:
        """Basic lexical ILIKE search over chunk text."""
        async with get_async_session() as session:
            sql = text("""
                SELECT
                    kc.id, kc.asset_id, kc.chunk_index, kc.text,
                    ka.title AS asset_title, ka.asset_type,
                    ka.source_filename, ka.version
                FROM knowledge_chunks kc
                JOIN knowledge_assets ka ON ka.id = kc.asset_id
                WHERE ka.status = :status
                  AND kc.text ILIKE :query
                LIMIT :top_k
            """)
            result = await session.execute(sql, {
                "query": f"%{query}%",
                "status": asset_status_filter,
                "top_k": top_k
            })
            rows = result.mappings().all()
            return [dict(r) for r in rows]

    # ─── IngestionJob ─────────────────────────────────────────

    async def save_job(self, job: IngestionJob) -> IngestionJob:
        async with get_async_session() as session:
            row = await session.get(DbIngestionJob, job.id)
            if row:
                row.asset_id = job.asset_id # type: ignore
                row.status = job.status.value # type: ignore
                row.current_stage = job.current_stage # type: ignore
                row.progress_pct = job.progress_pct # type: ignore
                row.updated_at = datetime.now(timezone.utc) # type: ignore
                row.error_message = job.error_message # type: ignore
                row.stage_log = [e.model_dump(mode="json") for e in job.stage_log] # type: ignore
                if job.completed_at:
                    row.completed_at = job.completed_at # type: ignore
            else:
                row = DbIngestionJob(
                    id=job.id,
                    asset_id=job.asset_id,
                    filename=job.filename,
                    file_type=job.file_type,
                    file_size_bytes=job.file_size_bytes,
                    status=job.status.value,
                    current_stage=job.current_stage,
                    progress_pct=job.progress_pct,
                    submitted_by=job.submitted_by,
                    stage_log=[],
                )
                session.add(row)
        return job

    async def get_job(self, job_id: str) -> IngestionJob:
        async with get_async_session() as session:
            row = await session.get(DbIngestionJob, job_id)
            if not row:
                raise NotFoundException(message=f"Ingestion job '{job_id}' not found.")
            return self._row_to_job(row)

    # ─── Candidates ───────────────────────────────────────────

    async def save_ontology_candidates(self, candidates: List[OntologyCandidate]) -> None:
        async with get_async_session() as session:
            for c in candidates:
                session.add(DbOntologyCandidate(
                    id=c.id, asset_id=c.asset_id, concept_id=c.concept_id,
                    concept_label=c.concept_label, confidence=c.confidence,
                    source_text_snippet=c.source_text_snippet, status=c.status.value
                ))

    async def get_ontology_candidates(self, asset_id: str) -> List[OntologyCandidate]:
        async with get_async_session() as session:
            stmt = select(DbOntologyCandidate).where(DbOntologyCandidate.asset_id == asset_id)
            result = await session.execute(stmt)
            return [self._row_to_oc(r) for r in result.scalars().all()]

    async def save_relationship_candidates(self, candidates: List[RelationshipCandidate]) -> None:
        async with get_async_session() as session:
            for c in candidates:
                session.add(DbRelationshipCandidate(
                    id=c.id, asset_id=c.asset_id,
                    source_entity_id=c.source_entity_id,
                    target_entity_id=c.target_entity_id,
                    target_entity_hint=c.target_entity_hint,
                    relationship_type=c.relationship_type,
                    confidence=c.confidence, status=c.status.value
                ))

    async def get_relationship_candidates(self, asset_id: str) -> List[RelationshipCandidate]:
        async with get_async_session() as session:
            stmt = select(DbRelationshipCandidate).where(DbRelationshipCandidate.asset_id == asset_id)
            result = await session.execute(stmt)
            return [self._row_to_rc(r) for r in result.scalars().all()]

    async def count_chunks_with_embeddings(self, asset_id: str) -> tuple[int, int]:
        """Returns (total_chunks, embedded_chunks) for an asset."""
        async with get_async_session() as session:
            total_result = await session.execute(
                text("SELECT COUNT(*) FROM knowledge_chunks WHERE asset_id = :aid"),
                {"aid": asset_id}
            )
            total = total_result.scalar() or 0

            embedded_result = await session.execute(
                text("SELECT COUNT(*) FROM knowledge_chunks WHERE asset_id = :aid AND embedding IS NOT NULL"),
                {"aid": asset_id}
            )
            embedded = embedded_result.scalar() or 0
            return int(total), int(embedded)

    # ─── Row converters ───────────────────────────────────────

    def _row_to_asset(self, row: DbKnowledgeAsset) -> KnowledgeAsset:
        return KnowledgeAsset(
            id=row.id, # type: ignore
            title=row.title, # type: ignore
            asset_type=row.asset_type, # type: ignore
            source_filename=row.source_filename, # type: ignore
            source_uri=row.source_uri, # type: ignore
            status=AssetStatus(row.status), # type: ignore
            version=row.version, # type: ignore
            language=row.language, # type: ignore
            entity_type_ref=row.entity_type_ref, # type: ignore
            department_owner=row.department_owner, # type: ignore
            created_by=row.created_by, # type: ignore
            created_at=row.created_at, # type: ignore
            updated_at=row.updated_at, # type: ignore
            published_at=row.published_at, # type: ignore
            archived_at=row.archived_at, # type: ignore
            extracted_metadata=row.extracted_metadata or {}, # type: ignore
            ontology_tags=row.ontology_tags or [], # type: ignore
            acl=row.acl or {}, # type: ignore
        )

    def _row_to_chunk(self, row: DbKnowledgeChunk) -> KnowledgeChunk:
        return KnowledgeChunk(
            id=row.id, # type: ignore
            asset_id=row.asset_id, # type: ignore
            chunk_index=row.chunk_index, # type: ignore
            chunk_strategy=ChunkStrategy(row.chunk_strategy), # type: ignore
            text=row.text, # type: ignore
            char_start=row.char_start, # type: ignore
            char_end=row.char_end, # type: ignore
            token_count=row.token_count, # type: ignore
            chunk_metadata=row.chunk_metadata or {}, # type: ignore
            embedding=row.embedding, # type: ignore
            embedding_model=row.embedding_model, # type: ignore
            embedding_version=row.embedding_version, # type: ignore
        )

    def _row_to_job(self, row: DbIngestionJob) -> IngestionJob:
        log_entries = [
            StageLogEntry(**e) for e in (row.stage_log or []) # type: ignore
        ]
        return IngestionJob(
            id=row.id, # type: ignore
            asset_id=row.asset_id, # type: ignore
            filename=row.filename, # type: ignore
            file_type=row.file_type, # type: ignore
            file_size_bytes=row.file_size_bytes, # type: ignore
            status=IngestionStatus(row.status), # type: ignore
            current_stage=row.current_stage, # type: ignore
            progress_pct=row.progress_pct, # type: ignore
            submitted_by=row.submitted_by, # type: ignore
            created_at=row.created_at, # type: ignore
            updated_at=row.updated_at, # type: ignore
            completed_at=row.completed_at, # type: ignore
            error_message=row.error_message, # type: ignore
            stage_log=log_entries,
        )

    def _row_to_oc(self, row: DbOntologyCandidate) -> OntologyCandidate:
        return OntologyCandidate(
            id=row.id, # type: ignore
            asset_id=row.asset_id, # type: ignore
            concept_id=row.concept_id, # type: ignore
            concept_label=row.concept_label, # type: ignore
            confidence=row.confidence, # type: ignore
            source_text_snippet=row.source_text_snippet, # type: ignore
            status=CandidateStatus(row.status), # type: ignore
        )

    def _row_to_rc(self, row: DbRelationshipCandidate) -> RelationshipCandidate:
        return RelationshipCandidate(
            id=row.id, # type: ignore
            asset_id=row.asset_id, # type: ignore
            source_entity_id=row.source_entity_id, # type: ignore
            target_entity_id=row.target_entity_id, # type: ignore
            target_entity_hint=row.target_entity_hint, # type: ignore
            relationship_type=row.relationship_type, # type: ignore
            confidence=row.confidence, # type: ignore
            status=CandidateStatus(row.status), # type: ignore
        )
