import uuid
import logging

from .monitor import ProcessingMonitor, ProcessingState
from .validation import DocumentValidator

logger = logging.getLogger("IngestionEngine")

class IngestionEngine:
    """The central entry point for uploading new knowledge to the enterprise system."""
    
    def __init__(self):
        self.monitor = ProcessingMonitor()
        self.validator = DocumentValidator()
        
    def receive_upload(self, file_path: str, department_owner: str) -> str:
        """
        Receives the file upload request, registers a tracking job, and begins validation.
        In production, this would drop the job onto a celery queue or Kafka topic.
        """
        job_id = str(uuid.uuid4())
        file_name = file_path.split("/")[-1]
        
        self.monitor.start_job(job_id, file_name)
        logger.info(f"Started ingestion job {job_id} for {file_name}")
        
        try:
            self.monitor.update_state(job_id, ProcessingState.VALIDATING, 10)
            self.validator.validate_file(file_path)
            
            # The file is valid. It would now be passed to the processing queue.
            self.monitor.update_state(job_id, ProcessingState.PARSING, 20)
            logger.info(f"Job {job_id} passed validation. Ready for parsing.")
            
            return job_id
            
        except ValueError as e:
            logger.error(f"Validation failed for job {job_id}: {e}")
            self.monitor.update_state(job_id, ProcessingState.FAILED, 10, error=str(e))
            raise e
