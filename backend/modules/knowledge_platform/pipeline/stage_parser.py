"""Stage 2 — Parser dispatch."""
import logging
from ..models import IngestionJob, IngestionStatus, StageLogEntry, KnowledgeAsset
from ..parsers.registry import ParserRegistry

logger = logging.getLogger("Pipeline.StageParser")


class ParserStage:
    def __init__(self, parser_registry: ParserRegistry):
        self.registry = parser_registry

    def run(self, job: IngestionJob, file_bytes: bytes,
            filename: str) -> tuple[IngestionJob, str]:
        """Returns (updated_job, extracted_text)."""
        job.current_stage = "PARSING"
        job.status = IngestionStatus.PARSING
        job.progress_pct = 15

        try:
            text = self.registry.parse(file_bytes, filename)
            job.stage_log.append(StageLogEntry(
                stage="PARSING", status="OK",
                message=f"Parsed {len(text)} characters from '{filename}'."
            ))
            logger.info(f"[{job.id}] Parsed {len(text)} chars from {filename}.")
            return job, text
        except NotImplementedError as e:
            job.status = IngestionStatus.FAILED
            job.error_message = str(e)
            job.stage_log.append(StageLogEntry(stage="PARSING", status="FAILED", message=str(e)))
            return job, ""
        except Exception as e:
            job.status = IngestionStatus.FAILED
            job.error_message = f"Parser error: {e}"
            job.stage_log.append(StageLogEntry(stage="PARSING", status="FAILED", message=str(e)))
            logger.error(f"[{job.id}] Parse failed: {e}")
            return job, ""
