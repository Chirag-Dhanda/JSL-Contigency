"""
Pipeline Orchestrator.
Manages the end-to-end execution of the ingestion lifecycle.
"""
import logging
from datetime import datetime, timezone
from ..models import IngestionJob, KnowledgeAsset, IngestionStatus
from ..repository import KnowledgeRepository
from ..parsers.registry import ParserRegistry

from .stage_upload import UploadStage
from .stage_parser import ParserStage
from .stage_chunker import ChunkerStage
from .stage_metadata import MetadataStage
from .stage_ontology import OntologyStage
from .stage_relationship import RelationshipStage
from .stage_embedding import EmbeddingStage
from modules.ontology.registry import OntologyRegistryService

logger = logging.getLogger("Pipeline.Orchestrator")


class IngestionPipelineOrchestrator:
    def __init__(self, 
                 repository: KnowledgeRepository,
                 parser_registry: ParserRegistry,
                 ontology_registry: OntologyRegistryService):
        self.repo = repository
        
        self.stage_upload = UploadStage()
        self.stage_parser = ParserStage(parser_registry)
        self.stage_chunker = ChunkerStage()
        self.stage_metadata = MetadataStage()
        self.stage_ontology = OntologyStage(ontology_registry)
        self.stage_relationship = RelationshipStage()
        self.stage_embedding = EmbeddingStage()

    async def execute_pipeline(self, job_id: str, file_bytes: bytes, filename: str, asset: KnowledgeAsset) -> IngestionJob:
        """
        Executes the entire ingestion pipeline synchronously (for EP-05).
        In a production scenario, this might be broken up into Celery tasks.
        """
        job = await self.repo.get_job(job_id)
        
        try:
            # 1. Upload/Validate
            job, asset = self.stage_upload.run(job, file_bytes, filename, asset)
            await self.repo.save_job(job)
            if job.status == IngestionStatus.FAILED:
                return job

            # 2. Parse
            job, text = self.stage_parser.run(job, file_bytes, filename)
            await self.repo.save_job(job)
            if job.status == IngestionStatus.FAILED:
                return job

            # 3. Chunk
            job, chunks = self.stage_chunker.run(job, text, asset)
            await self.repo.save_job(job)
            if job.status == IngestionStatus.FAILED:
                return job

            # 4. Metadata
            job, asset = self.stage_metadata.run(job, text, asset)
            await self.repo.save_asset(asset) # Persist extracted metadata early
            await self.repo.save_job(job)
            if job.status == IngestionStatus.FAILED:
                return job

            # 5. Ontology
            job, ontology_cands = self.stage_ontology.run(job, text, asset)
            await self.repo.save_ontology_candidates(ontology_cands)
            await self.repo.save_job(job)
            if job.status == IngestionStatus.FAILED:
                return job

            # 6. Relationships
            job, rel_cands = self.stage_relationship.run(job, text, asset)
            await self.repo.save_relationship_candidates(rel_cands)
            await self.repo.save_job(job)
            if job.status == IngestionStatus.FAILED:
                return job

            # 7. Embedding
            job, embedded_chunks = await self.stage_embedding.run(job, chunks)
            # Save chunks to DB (this includes the pgvector text!)
            await self.repo.save_chunks(embedded_chunks)
            await self.repo.save_job(job)
            if job.status == IngestionStatus.FAILED:
                return job

            # Pipeline Success!
            job.status = IngestionStatus.REVIEW
            job.current_stage = "REVIEW"
            job.progress_pct = 100
            job.completed_at = datetime.now(timezone.utc)
            
            asset.status = "REVIEW" # type: ignore
            await self.repo.save_asset(asset)
            await self.repo.save_job(job)
            
            logger.info(f"[{job.id}] Pipeline completed successfully. Asset ready for review.")
            return job

        except Exception as e:
            logger.error(f"[{job.id}] Unhandled pipeline exception: {e}", exc_info=True)
            job.status = IngestionStatus.FAILED
            job.error_message = f"Unhandled error: {str(e)}"
            await self.repo.save_job(job)
            return job
