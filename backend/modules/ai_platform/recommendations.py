"""
AI Recommendation Engine (EP-08).
Generates non-autonomous recommendations using metadata and graph traversal.
AI never makes automatic decisions — all recommendations require user review.
"""
import logging
from typing import List, Optional, Dict, Any

logger = logging.getLogger("AIPlatform.Recommendations")


class AIRecommendation:
    def __init__(self, category: str, title: str, reason: str, entity_id: Optional[str] = None, confidence: float = 0.0):
        self.category = category
        self.title = title
        self.reason = reason
        self.entity_id = entity_id
        self.confidence = round(confidence, 3)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "title": self.title,
            "reason": self.reason,
            "entity_id": self.entity_id,
            "confidence": self.confidence,
            "requires_review": True  # Always True — no autonomous actions
        }


class AIRecommendationEngine:
    """
    Generates enterprise recommendations via metadata + graph traversal.
    Uses no raw LLM reasoning for recommendations — factual metadata only.
    """

    def generate_for_context(
        self,
        query: str,
        user_department: Optional[str],
        context_asset_ids: List[str]
    ) -> List[AIRecommendation]:
        """
        Generates recommendations based on the assets retrieved in a context package.
        
        For EP-08 MVP: Heuristic-based recommendations derived from query keywords and dept.
        Future: Full graph traversal via Neo4j for semantic relationship-based suggestions.
        """
        recommendations: List[AIRecommendation] = []
        query_lower = query.lower()

        # Related Documents (keyword-based for MVP)
        if any(kw in query_lower for kw in ["sop", "procedure", "process", "standard"]):
            recommendations.append(AIRecommendation(
                category="RELATED_DOCUMENT",
                title="Standard Operating Procedures",
                reason="Your query mentions process or procedure keywords.",
                confidence=0.7
            ))

        # Learning Modules
        if any(kw in query_lower for kw in ["how to", "training", "learn", "guide"]):
            recommendations.append(AIRecommendation(
                category="LEARNING_MODULE",
                title=f"Training resources for {user_department or 'your department'}",
                reason="Your query indicates a learning intent.",
                confidence=0.65
            ))

        # Safety
        if any(kw in query_lower for kw in ["safety", "hazard", "risk", "incident"]):
            recommendations.append(AIRecommendation(
                category="RELATED_DOCUMENT",
                title="Safety & Hazard Register",
                reason="Your query relates to safety — review the current safety register.",
                confidence=0.8
            ))

        # Related Workflow
        if any(kw in query_lower for kw in ["approve", "workflow", "review", "submit"]):
            recommendations.append(AIRecommendation(
                category="WORKFLOW",
                title="Document Approval Workflow",
                reason="Your query suggests a document approval process may be applicable.",
                confidence=0.6
            ))

        # Context-based (related documents from retrieved assets)
        if context_asset_ids:
            recommendations.append(AIRecommendation(
                category="RELATED_DOCUMENT",
                title="Related Enterprise Documents",
                reason=f"Based on {len(context_asset_ids)} retrieved knowledge assets related to your query.",
                confidence=0.75
            ))

        return recommendations
