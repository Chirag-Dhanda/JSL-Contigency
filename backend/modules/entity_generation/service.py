import logging
from modules.knowledge_intake.models import IntakeJob, ProposedEntity

logger = logging.getLogger("EntityGeneration")

class EntityGenerationService:
    """
    Simulates an LLM analyzing the extracted text to propose new business entities.
    """
    
    def process(self, job: IntakeJob) -> IntakeJob:
        logger.info(f"Generating entities for: {job.filename}")
        
        # Mock entity generation based on Document Type
        
        # 1. The document itself becomes an entity
        doc_entity = ProposedEntity(
            entity_type="sop" if job.document_type == "SOP" else "lesson" if job.document_type == "LESSON" else "safety_doc",
            display_name=job.filename.split('.')[0].replace('_', ' ').title(),
            proposed_metadata={
                "version": "1.0",
                "source_file": job.filename
            }
        )
        job.proposed_entities.append(doc_entity)
        
        # 2. Extract embedded entities (e.g., Equipment mentioned in the text)
        if "EAF" in job.filename.upper() or "FURNACE" in job.filename.upper():
            eq_entity = ProposedEntity(
                entity_type="equipment",
                display_name="Electric Arc Furnace - Proposed",
                proposed_metadata={"status": "UNKNOWN"}
            )
            job.proposed_entities.append(eq_entity)
            
        logger.info(f"Generated {len(job.proposed_entities)} entities.")
        return job
