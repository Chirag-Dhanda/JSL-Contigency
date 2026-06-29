"""Stage 6 — Relationship Candidate Detection."""
import logging
from typing import List
from ..models import IngestionJob, IngestionStatus, StageLogEntry, KnowledgeAsset, RelationshipCandidate

logger = logging.getLogger("Pipeline.StageRelationship")


class RelationshipStage:
    def run(self, job: IngestionJob, text: str, asset: KnowledgeAsset) -> tuple[IngestionJob, List[RelationshipCandidate]]:
        job.current_stage = "RELATIONSHIP_DISCOVERY"
        job.status = IngestionStatus.RELATIONSHIP_DISCOVERY
        job.progress_pct = 60

        try:
            candidates: List[RelationshipCandidate] = []
            
            # Simple heuristic for EP-05: Look for department ownership matches
            # or explicit document cross-references (e.g. "SOP-123")
            # For now, we will create a mock relation based on department
            if asset.department_owner:
                candidates.append(RelationshipCandidate(
                    asset_id=asset.id,
                    source_entity_id=asset.id,
                    target_entity_hint=asset.department_owner,
                    relationship_type="OWNED_BY_DEPARTMENT",
                    confidence=0.9
                ))

            job.stage_log.append(StageLogEntry(
                stage="RELATIONSHIP_DISCOVERY", status="OK",
                message=f"Generated {len(candidates)} relationship candidates."
            ))
            logger.info(f"[{job.id}] Generated {len(candidates)} relationship candidates.")
            return job, candidates
        except Exception as e:
            job.status = IngestionStatus.FAILED
            job.error_message = f"Relationship discovery failed: {e}"
            job.stage_log.append(StageLogEntry(stage="RELATIONSHIP_DISCOVERY", status="FAILED", message=str(e)))
            logger.error(f"[{job.id}] Relationship discovery failed: {e}")
            return job, []
