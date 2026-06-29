"""
Ranking Engine for Enterprise Search (EP-06).
"""
import logging
from typing import List, Dict, Any
from .models import RetrievalPlan, RankedPassage

logger = logging.getLogger("SearchEngine.Ranking")


class ConfigurableRankingEngine:
    """
    Ranks raw hits based on strategy weights defined in the RetrievalPlan.
    """

    def rank(self, raw_results: Dict[str, Any], plan: RetrievalPlan) -> List[RankedPassage]:
        weights = {s.name: s.weight for s in plan.strategies if s.enabled}
        
        w_vec = weights.get("vector", 0.0)
        w_lex = weights.get("lexical", 0.0)
        w_graph = weights.get("graph", 0.0)
        w_ont = weights.get("ontology", 0.0)

        passages: List[RankedPassage] = []

        for cid, data in raw_results.items():
            # Calculate final weighted score
            final_score = (
                (data["vector_score"] * w_vec) +
                (data["lexical_score"] * w_lex) +
                (data["graph_score"] * w_graph) +
                (data["ontology_score"] * w_ont)
            )

            passages.append(RankedPassage(
                id=data["id"],
                asset_id=data["asset_id"],
                asset_title=data["asset_title"],
                asset_type=data["asset_type"],
                chunk_index=data["chunk_index"],
                text=data["text"],
                final_score=round(final_score, 4),
                lexical_score=round(data["lexical_score"], 4),
                vector_score=round(data["vector_score"], 4),
                graph_score=round(data["graph_score"], 4),
                ontology_score=round(data["ontology_score"], 4),
                source_filename=data.get("source_filename"),
                version=data.get("version", 1)
            ))

        # Sort descending by final score
        passages.sort(key=lambda p: p.final_score, reverse=True)
        return passages
