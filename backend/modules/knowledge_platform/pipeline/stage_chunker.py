"""Stage 3 — Text Chunking."""
import logging
from typing import List
from ..models import IngestionJob, IngestionStatus, StageLogEntry, KnowledgeAsset, KnowledgeChunk, ChunkStrategy

logger = logging.getLogger("Pipeline.StageChunker")


class ChunkerStage:
    def __init__(self, default_chunk_size: int = 500, default_overlap: int = 50):
        self.chunk_size = default_chunk_size
        self.overlap = default_overlap

    def run(self, job: IngestionJob, text: str, asset: KnowledgeAsset) -> tuple[IngestionJob, List[KnowledgeChunk]]:
        job.current_stage = "CHUNKING"
        job.status = IngestionStatus.CHUNKING
        job.progress_pct = 30

        if not text.strip():
            job.status = IngestionStatus.FAILED
            job.error_message = "Parsed text is empty."
            job.stage_log.append(StageLogEntry(stage="CHUNKING", status="FAILED", message="Empty text."))
            return job, []

        try:
            chunks = self._chunk_fixed(text, asset.id)
            job.stage_log.append(StageLogEntry(
                stage="CHUNKING", status="OK",
                message=f"Generated {len(chunks)} chunks using FIXED strategy."
            ))
            logger.info(f"[{job.id}] Generated {len(chunks)} chunks.")
            return job, chunks
        except Exception as e:
            job.status = IngestionStatus.FAILED
            job.error_message = f"Chunking failed: {e}"
            job.stage_log.append(StageLogEntry(stage="CHUNKING", status="FAILED", message=str(e)))
            logger.error(f"[{job.id}] Chunking failed: {e}")
            return job, []

    def _chunk_fixed(self, text: str, asset_id: str) -> List[KnowledgeChunk]:
        """Simple fixed-length word chunking with overlap."""
        words = text.split()
        chunks: List[KnowledgeChunk] = []
        i = 0
        chunk_index = 0

        # Create basic word-level approximation for character offsets
        # Real char offsets require traversing the string exactly
        # This is a basic implementation for EP-05
        char_idx = 0

        while i < len(words):
            end_index = min(i + self.chunk_size, len(words))
            chunk_words = words[i:end_index]
            chunk_text = " ".join(chunk_words)
            
            # Approximate char_start
            start = text.find(chunk_words[0], char_idx) if chunk_words else 0
            if start != -1:
                char_idx = start

            chunks.append(KnowledgeChunk(
                asset_id=asset_id,
                chunk_index=chunk_index,
                chunk_strategy=ChunkStrategy.FIXED,
                text=chunk_text,
                char_start=char_idx,
                char_end=char_idx + len(chunk_text),
                token_count=len(chunk_words) # rough proxy
            ))

            i += (self.chunk_size - self.overlap)
            chunk_index += 1
            if i >= len(words):
                break

        return chunks
