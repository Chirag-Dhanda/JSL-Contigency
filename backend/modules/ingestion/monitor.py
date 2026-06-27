from enum import Enum
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProcessingState(str, Enum):
    RECEIVED = "RECEIVED"
    VALIDATING = "VALIDATING"
    PARSING = "PARSING"
    CLEANING = "CLEANING"
    CHUNKING = "CHUNKING"
    INDEXING = "INDEXING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ProcessingStatus(BaseModel):
    job_id: str
    file_name: str
    current_state: ProcessingState
    progress_percentage: int
    started_at: datetime
    updated_at: datetime
    errors: List[str] = []
    warnings: List[str] = []

class ProcessingMonitor:
    """Tracks the lifecycle of a document moving through the ingestion pipeline."""
    
    def __init__(self):
        # In a real environment, this would be backed by Redis or a DB table
        self.jobs = {}
        
    def start_job(self, job_id: str, file_name: str) -> ProcessingStatus:
        now = datetime.utcnow()
        status = ProcessingStatus(
            job_id=job_id,
            file_name=file_name,
            current_state=ProcessingState.RECEIVED,
            progress_percentage=0,
            started_at=now,
            updated_at=now
        )
        self.jobs[job_id] = status
        return status
        
    def update_state(self, job_id: str, state: ProcessingState, progress: int, error: Optional[str] = None):
        if job_id in self.jobs:
            self.jobs[job_id].current_state = state
            self.jobs[job_id].progress_percentage = progress
            self.jobs[job_id].updated_at = datetime.utcnow()
            if error:
                self.jobs[job_id].errors.append(error)
                self.jobs[job_id].current_state = ProcessingState.FAILED
