"""
Stage 1 — Upload Validation
Validates MIME type, file size, extension before ingestion begins.
"""
import os
import logging
from ..models import IngestionJob, IngestionStatus, StageLogEntry, KnowledgeAsset

logger = logging.getLogger("Pipeline.StageUpload")

ALLOWED_EXTENSIONS = {
    ".pdf", ".docx", ".doc", ".txt", ".md", ".markdown",
    ".rst", ".csv", ".json", ".tsv", ".jpg", ".jpeg",
    ".png", ".tiff", ".bmp"
}
MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB


class UploadStage:
    def run(self, job: IngestionJob, file_bytes: bytes, filename: str,
            asset: KnowledgeAsset) -> tuple[IngestionJob, KnowledgeAsset]:

        job.current_stage = "VALIDATING"
        job.status = IngestionStatus.VALIDATING
        job.progress_pct = 5

        ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

        # 1. Extension check
        if ext not in ALLOWED_EXTENSIONS:
            job.status = IngestionStatus.FAILED
            job.error_message = f"File extension '{ext}' is not permitted."
            job.stage_log.append(StageLogEntry(stage="VALIDATING", status="FAILED",
                                               message=job.error_message))
            return job, asset

        # 2. Size check
        file_size = len(file_bytes)
        if file_size > MAX_FILE_SIZE_BYTES:
            job.status = IngestionStatus.FAILED
            job.error_message = f"File size {file_size} bytes exceeds limit of {MAX_FILE_SIZE_BYTES}."
            job.stage_log.append(StageLogEntry(stage="VALIDATING", status="FAILED",
                                               message=job.error_message))
            return job, asset

        # 3. Non-empty check
        if file_size == 0:
            job.status = IngestionStatus.FAILED
            job.error_message = "Uploaded file is empty."
            job.stage_log.append(StageLogEntry(stage="VALIDATING", status="FAILED",
                                               message=job.error_message))
            return job, asset

        # Update job and asset
        job.file_size_bytes = file_size
        asset.source_filename = filename
        job.stage_log.append(StageLogEntry(stage="VALIDATING", status="OK",
                                           message=f"File validated: {filename} ({file_size} bytes)"))
        logger.info(f"[{job.id}] Upload validation passed: {filename}")
        return job, asset
