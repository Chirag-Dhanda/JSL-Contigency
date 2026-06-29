"""
Master Editor Review Workspace logic.
Generates comprehensive review packages before an asset can be published.
"""
import logging
from .models import KnowledgeAsset, KnowledgeReviewPackage
from .repository import KnowledgeRepository
from .quality import KnowledgeQualityService

logger = logging.getLogger("KnowledgePlatform.Review")


class KnowledgeReviewService:
    def __init__(self, repo: KnowledgeRepository, quality_svc: KnowledgeQualityService):
        self.repo = repo
        self.quality_svc = quality_svc

    async def generate_review_package(self, asset: KnowledgeAsset) -> KnowledgeReviewPackage:
        logger.info(f"Generating review package for Asset {asset.id}")

        # 1. Fetch Candidates
        ont_cands = await self.repo.get_ontology_candidates(asset.id)
        rel_cands = await self.repo.get_relationship_candidates(asset.id)

        # 2. Embedding Coverage
        total_chunks, embedded_chunks = await self.repo.count_chunks_with_embeddings(asset.id)
        coverage_pct = (embedded_chunks / total_chunks * 100.0) if total_chunks > 0 else 0.0

        # 3. Quality Score
        quality_score = await self.quality_svc.calculate_quality_score(asset)

        # 4. Duplicate Detection (Basic mock for EP-05)
        duplicate_warnings = []
        conflicts = []
        if total_chunks > 0 and embedded_chunks > 0:
            # We could fetch the first chunk and do a semantic search
            # For this MVP, we simulate passing unless it's explicitly broken.
            pass

        # 5. Recommendation logic
        if quality_score < 0.3:
            recommendation = "REJECT"
            conflicts.append("Quality score is below minimum threshold (0.3).")
        elif coverage_pct < 90.0:
            recommendation = "REVIEW_REQUIRED"
            conflicts.append(f"Low embedding coverage: {coverage_pct}%.")
        elif not ont_cands:
            recommendation = "REVIEW_REQUIRED"
            duplicate_warnings.append("No ontology candidates found. Ensure document is discoverable.")
        else:
            recommendation = "APPROVE"

        return KnowledgeReviewPackage(
            asset_id=asset.id,
            asset_title=asset.title,
            asset_status=asset.status,
            extracted_metadata=asset.extracted_metadata,
            ontology_candidates=ont_cands,
            relationship_candidates=rel_cands,
            chunk_count=total_chunks,
            embedded_chunk_count=embedded_chunks,
            embedding_coverage_pct=coverage_pct,
            quality_score=quality_score,
            duplicate_warnings=duplicate_warnings,
            conflicts=conflicts,
            recommendation=recommendation
        )
