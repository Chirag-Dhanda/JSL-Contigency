import logging
from typing import Dict, List, Optional
from modules.knowledge_intake.models import IntakeJob, ProposedEntity, ProposedRelationship
from modules.metadata_engine.service import MetadataEngineService
from modules.relationship_engine.service import RelationshipEngineService
from exceptions.base import SystemException, NotFoundException

logger = logging.getLogger("ReviewEngine")

class ReviewEngineService:
    """
    Manages the Review Queue where AI-proposed entities and relationships 
    wait for Master Editor approval before entering the live Knowledge Graph.
    """
    def __init__(self, metadata_engine: MetadataEngineService, relationship_engine: RelationshipEngineService):
        self.meta_engine = metadata_engine
        self.rel_engine = relationship_engine
        self._queue: Dict[str, IntakeJob] = {}
        logger.info("Review Engine Initialized.")

    def submit_for_review(self, job: IntakeJob):
        job.status = "IN_REVIEW"
        self._queue[job.id] = job
        logger.info(f"Intake Job {job.id} submitted to Review Queue.")

    def get_pending_jobs(self) -> List[IntakeJob]:
        return [job for job in self._queue.values() if job.status == "IN_REVIEW"]
        
    def get_job(self, job_id: str) -> IntakeJob:
        if job_id not in self._queue:
            raise NotFoundException(message=f"Job {job_id} not found in Review Engine.")
        return self._queue[job_id]

    def approve_job(self, job_id: str, editor_id: str):
        job = self.get_job(job_id)
        if job.status != "IN_REVIEW":
            raise SystemException(message=f"Job {job_id} is not in review state.")
            
        logger.info(f"Master Editor '{editor_id}' approving job {job_id}...")
        
        # 1. Map proposed IDs to Live IDs
        id_mapping: Dict[str, str] = {}
        
        # 2. Commit Entities
        for prop_ent in job.proposed_entities:
            if prop_ent.status == "PENDING":
                live_ent = self.meta_engine.create_entity(
                    name=prop_ent.id, # Keep ID for simplicity in mapping
                    entity_type=prop_ent.entity_type,
                    display_name=prop_ent.display_name,
                    created_by=editor_id,
                    metadata=prop_ent.proposed_metadata
                )
                id_mapping[prop_ent.id] = live_ent.id
                prop_ent.status = "APPROVED"
                
        # 3. Commit Relationships
        for prop_rel in job.proposed_relationships:
            # Resolve source and target IDs in case they were newly created
            source = id_mapping.get(prop_rel.source_id, prop_rel.source_id)
            target = id_mapping.get(prop_rel.target_id, prop_rel.target_id)
            
            self.rel_engine.create_relationship(
                source_id=source,
                target_id=target,
                rel_type=prop_rel.relationship_type,
                created_by=editor_id
            )
            
        job.status = "COMPLETED"
        logger.info(f"Job {job_id} successfully committed to Knowledge Graph.")

    def reject_job(self, job_id: str, editor_id: str):
        job = self.get_job(job_id)
        job.status = "REJECTED"
        logger.info(f"Master Editor '{editor_id}' rejected job {job_id}.")
