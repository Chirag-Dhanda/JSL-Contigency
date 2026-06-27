import logging
from modules.knowledge_intake.models import IntakeJob

logger = logging.getLogger("DocumentUnderstanding")

class DocumentUnderstandingService:
    """
    Simulates an AI document parser that classifies the document type, language, and extracts text.
    """
    
    def process(self, job: IntakeJob) -> IntakeJob:
        logger.info(f"Understanding document: {job.filename}")
        
        # Mock AI extraction logic
        if "manual" in job.filename.lower() or "sop" in job.filename.lower():
            job.document_type = "SOP"
        elif "training" in job.filename.lower() or "lesson" in job.filename.lower():
            job.document_type = "LESSON"
        elif "policy" in job.filename.lower():
            job.document_type = "POLICY"
        else:
            job.document_type = "GENERAL_DOCUMENT"
            
        job.language = "en"
        job.extracted_text = f"Mock extracted content from {job.filename}. Discusses safety protocols and machine operation."
        
        logger.info(f"Classified as {job.document_type}")
        return job
