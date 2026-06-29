"""
Knowledge Quality Engine.
Calculates metrics (Completeness, Freshness, Coverage) for knowledge assets.
"""
import logging
from datetime import datetime, timezone
from .models import KnowledgeAsset
from .repository import KnowledgeRepository

logger = logging.getLogger("KnowledgePlatform.Quality")


class KnowledgeQualityService:
    def __init__(self, repo: KnowledgeRepository):
        self.repo = repo

    async def calculate_quality_score(self, asset: KnowledgeAsset) -> float:
        """
        Returns a score between 0.0 and 1.0 based on EP-05 quality metrics.
        """
        score = 0.0
        weights = {
            "completeness": 0.4,
            "freshness": 0.2,
            "coverage": 0.4
        }

        # 1. Completeness (Are basic metadata fields filled?)
        metadata_score = 0.0
        if asset.title: metadata_score += 0.25
        if asset.department_owner: metadata_score += 0.25
        if asset.extracted_metadata.get("auto_title"): metadata_score += 0.25
        if asset.extracted_metadata.get("word_count", 0) > 0: metadata_score += 0.25
        score += (metadata_score * weights["completeness"])

        # 2. Freshness
        # Decay over 1 year (365 days)
        now = datetime.now(timezone.utc)
        age_days = (now - asset.updated_at).days
        freshness_score = max(0.0, 1.0 - (age_days / 365.0))
        score += (freshness_score * weights["freshness"])

        # 3. Coverage (What % of chunks have embeddings?)
        total, embedded = await self.repo.count_chunks_with_embeddings(asset.id)
        coverage_score = (embedded / total) if total > 0 else 0.0
        score += (coverage_score * weights["coverage"])

        return round(score, 4)
