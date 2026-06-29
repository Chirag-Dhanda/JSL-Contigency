"""Stage 5 — Ontology Candidate Detection."""
import logging
from typing import List
from ..models import IngestionJob, IngestionStatus, StageLogEntry, KnowledgeAsset, OntologyCandidate
from modules.ontology.registry import OntologyRegistryService

logger = logging.getLogger("Pipeline.StageOntology")


class OntologyStage:
    def __init__(self, registry: OntologyRegistryService):
        self.registry = registry

    def run(self, job: IngestionJob, text: str, asset: KnowledgeAsset) -> tuple[IngestionJob, List[OntologyCandidate]]:
        job.current_stage = "ONTOLOGY_MAPPING"
        job.status = IngestionStatus.ONTOLOGY_MAPPING
        job.progress_pct = 50

        try:
            # 1. Fetch concepts (in a real system, this might be cached/indexed)
            concepts = self.registry.list_concepts()
            candidates: List[OntologyCandidate] = []
            
            # 2. Simple lexical scan for concept labels in text
            text_lower = text.lower()
            for concept in concepts:
                if concept.display_name.lower() in text_lower:
                    # Find a short snippet for context
                    idx = text_lower.find(concept.display_name.lower())
                    start = max(0, idx - 50)
                    end = min(len(text), idx + len(concept.display_name) + 50)
                    snippet = text[start:end].replace('\n', ' ')

                    candidates.append(OntologyCandidate(
                        asset_id=asset.id,
                        concept_id=concept.concept_id,
                        concept_label=concept.display_name,
                        confidence=0.8, # simple exact match
                        source_text_snippet=snippet.strip()
                    ))

            job.stage_log.append(StageLogEntry(
                stage="ONTOLOGY_MAPPING", status="OK",
                message=f"Found {len(candidates)} ontology candidates."
            ))
            logger.info(f"[{job.id}] Found {len(candidates)} ontology candidates.")
            return job, candidates
        except Exception as e:
            job.status = IngestionStatus.FAILED
            job.error_message = f"Ontology mapping failed: {e}"
            job.stage_log.append(StageLogEntry(stage="ONTOLOGY_MAPPING", status="FAILED", message=str(e)))
            logger.error(f"[{job.id}] Ontology mapping failed: {e}")
            return job, []
