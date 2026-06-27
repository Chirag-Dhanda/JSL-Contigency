import logging
import asyncio
from typing import List
from modules.knowledge_intake.models import IntakeJob
from modules.document_understanding.service import DocumentUnderstandingService
from modules.entity_generation.service import EntityGenerationService
from modules.relationship_discovery.service import RelationshipDiscoveryService
from modules.review_engine.service import ReviewEngineService

logger = logging.getLogger("AIKnowledgeArchitect")

class KnowledgeArchitectOrchestrator:
    """
    The Master AI Pipeline Orchestrator. 
    It receives an Intake Job (e.g. from a file upload), runs it through the 
    understanding and generation pipeline, and submits it to the Review Queue.
    """
    
    def __init__(self, review_engine: ReviewEngineService):
        self.doc_service = DocumentUnderstandingService()
        self.ent_service = EntityGenerationService()
        self.rel_service = RelationshipDiscoveryService()
        self.review_engine = review_engine
        
        # Keep track of active jobs
        self._jobs: dict[str, IntakeJob] = {}
        logger.info("AI Knowledge Architect Orchestrator Initialized.")

    def ingest_file(self, filename: str, file_type: str, uploader: str) -> IntakeJob:
        """Entrypoint for the Intake Pipeline."""
        job = IntakeJob(
            filename=filename, 
            file_type=file_type, 
            uploaded_by=uploader
        )
        self._jobs[job.id] = job
        logger.info(f"Started Intake Job {job.id} for {filename}")
        
        # Fire and forget the pipeline processing
        asyncio.create_task(self._run_pipeline(job.id))
        
        return job

    async def _run_pipeline(self, job_id: str):
        job = self._jobs.get(job_id)
        if not job:
            return
            
        try:
            # 1. Document Understanding
            job = self.doc_service.process(job)
            
            # 2. Entity Generation
            job = self.ent_service.process(job)
            
            # 3. Relationship Discovery (including SAP mappings)
            job = self.rel_service.process(job)
            
            # 4. Generate AI Summary
            job.ai_summary = f"Analyzed {job.document_type} document. Proposed {len(job.proposed_entities)} entities and {len(job.proposed_relationships)} connections. Prepared {job.sap_placeholders_created} SAP mapping placeholders."
            
            # 5. Submit to Master Review Queue
            self.review_engine.submit_for_review(job)
            logger.info(f"Job {job.id} pipeline completed. Awaiting Master Editor review.")
            
        except Exception as e:
            logger.error(f"Job {job.id} failed during AI Pipeline processing: {e}")
            job.status = "FAILED"
            
    def get_job_status(self, job_id: str) -> IntakeJob:
        return self._jobs.get(job_id)
