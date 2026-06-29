"""Stage 7 — Vector Embeddings."""
import logging
from typing import List
from ..models import IngestionJob, IngestionStatus, StageLogEntry, KnowledgeChunk
from modules.embeddings.provider import embedding_provider

logger = logging.getLogger("Pipeline.StageEmbedding")


class EmbeddingStage:
    async def run(self, job: IngestionJob, chunks: List[KnowledgeChunk]) -> tuple[IngestionJob, List[KnowledgeChunk]]:
        job.current_stage = "EMBEDDING"
        job.status = IngestionStatus.EMBEDDING
        job.progress_pct = 75

        try:
            # Batch embedding generation
            # For robustness in EP-05, we generate embeddings one by one to avoid huge payloads
            # falling over, but ideally this would be batched.
            success_count = 0
            for i, chunk in enumerate(chunks):
                vec = await embedding_provider.get_embedding(chunk.text)
                if vec:
                    chunk.embedding = vec
                    chunk.embedding_model = embedding_provider.model
                    chunk.embedding_version = 1
                    success_count += 1
                
                # Update progress
                job.progress_pct = 75 + int((i / len(chunks)) * 15)

            job.stage_log.append(StageLogEntry(
                stage="EMBEDDING", status="OK",
                message=f"Generated embeddings for {success_count}/{len(chunks)} chunks."
            ))
            logger.info(f"[{job.id}] Embedded {success_count}/{len(chunks)} chunks.")
            return job, chunks
        except Exception as e:
            job.status = IngestionStatus.FAILED
            job.error_message = f"Embedding generation failed: {e}"
            job.stage_log.append(StageLogEntry(stage="EMBEDDING", status="FAILED", message=str(e)))
            logger.error(f"[{job.id}] Embedding generation failed: {e}")
            return job, chunks
