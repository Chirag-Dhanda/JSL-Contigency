"""Stage 4 — Metadata Extraction."""
import logging
import re
from typing import Dict, Any
from ..models import IngestionJob, IngestionStatus, StageLogEntry, KnowledgeAsset

logger = logging.getLogger("Pipeline.StageMetadata")


class MetadataStage:
    def run(self, job: IngestionJob, text: str, asset: KnowledgeAsset) -> tuple[IngestionJob, KnowledgeAsset]:
        job.current_stage = "EXTRACTING"
        job.status = IngestionStatus.EXTRACTING
        job.progress_pct = 40

        try:
            # 1. Title Extraction
            # Very basic heuristic: First non-empty line
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            if lines and not asset.title:
                # Truncate title if it's too long
                asset.title = lines[0][:200]
            elif not asset.title:
                asset.title = asset.source_filename or "Untitled Asset"

            # 2. Keyword extraction (Basic regex heuristics for EP-05)
            # Find capitalized words (excluding common start-of-sentence) or specific patterns
            # Here we just implement a very basic extraction for structural completion
            words = text.split()
            unique_words = set(w.lower().strip(".,:;()[]\"'") for w in words if len(w) > 5)
            # A real system might use tf-idf or NLP. We store an empty structure for now.
            
            asset.extracted_metadata = {
                "auto_title": lines[0][:200] if lines else None,
                "word_count": len(words),
                "char_count": len(text),
                "extracted_keywords": list(unique_words)[:10] # just random long words
            }

            job.stage_log.append(StageLogEntry(
                stage="EXTRACTING", status="OK",
                message="Extracted basic metadata."
            ))
            logger.info(f"[{job.id}] Extracted metadata.")
            return job, asset
        except Exception as e:
            job.status = IngestionStatus.FAILED
            job.error_message = f"Metadata extraction failed: {e}"
            job.stage_log.append(StageLogEntry(stage="EXTRACTING", status="FAILED", message=str(e)))
            logger.error(f"[{job.id}] Metadata extraction failed: {e}")
            return job, asset
