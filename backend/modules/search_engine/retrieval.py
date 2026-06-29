"""
Hybrid Retrieval Engine (EP-06).
Executes searches across Lexical, Vector, and Graph axes based on a RetrievalPlan.
"""
import logging
from typing import List, Dict, Any

from modules.knowledge_platform.repository import KnowledgeRepository
from modules.relationship_engine.neo4j_repository import Neo4jRepository
from modules.embeddings.provider import embedding_provider
from .models import SearchRequest, RetrievalPlan

logger = logging.getLogger("SearchEngine.Retrieval")


class HybridRetrievalEngine:
    def __init__(self, pg_repo: KnowledgeRepository, graph_repo: Neo4jRepository):
        self.pg_repo = pg_repo
        self.graph_repo = graph_repo

    async def execute(self, request: SearchRequest, plan: RetrievalPlan) -> Dict[str, Any]:
        """
        Executes the required searches and aggregates raw results.
        Returns a dict of {chunk_id: raw_result_dict}.
        """
        raw_results: Dict[str, Any] = {}
        
        strategy_names = [s.name for s in plan.strategies if s.enabled]
        top_k_pool = request.max_results * 3  # Retrieve wider pool for reranking

        # 1. Vector Search
        if "vector" in strategy_names:
            query_vector = await embedding_provider.get_embedding(plan.optimized_query)
            if query_vector:
                vec_hits = await self.pg_repo.semantic_search(query_vector, top_k=top_k_pool)
                for hit in vec_hits:
                    cid = hit["id"]
                    if cid not in raw_results:
                        raw_results[cid] = self._base_hit(hit)
                    
                    # Convert distance to a similarity score (0 to 1ish)
                    dist = hit.get("distance", 1.0)
                    raw_results[cid]["vector_score"] = max(0.0, 1.0 - (dist / 2.0))

        # 2. Lexical Search
        if "lexical" in strategy_names:
            lex_hits = await self.pg_repo.lexical_search(plan.optimized_query, top_k=top_k_pool)
            for hit in lex_hits:
                cid = hit["id"]
                if cid not in raw_results:
                    raw_results[cid] = self._base_hit(hit)
                
                # Mock TF-IDF/BM25 score for EP-06 (lexical hit = 0.5 flat bump)
                raw_results[cid]["lexical_score"] = 0.5

        # 3. Graph Expansion / Ontology Hinting
        # In a full implementation, we pass the extracted asset_ids to Neo4j to boost
        # assets that are closely linked to the user's department or queried concepts.
        if "graph" in strategy_names or "ontology" in strategy_names:
            asset_ids = list(set([r["asset_id"] for r in raw_results.values()]))
            # For EP-06 MVP, we simulate a slight graph boost for matching departments
            for cid, data in raw_results.items():
                # If asset type matches requested, slight bump
                if data["asset_type"] in plan.target_asset_types:
                    data["graph_score"] = 0.2
                else:
                    data["graph_score"] = 0.0
                    
        return raw_results

    def _base_hit(self, hit: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": hit["id"],
            "asset_id": hit["asset_id"],
            "asset_title": hit["asset_title"],
            "asset_type": hit["asset_type"],
            "chunk_index": hit["chunk_index"],
            "text": hit["text"],
            "source_filename": hit.get("source_filename"),
            "version": hit.get("version", 1),
            "vector_score": 0.0,
            "lexical_score": 0.0,
            "graph_score": 0.0,
            "ontology_score": 0.0
        }
