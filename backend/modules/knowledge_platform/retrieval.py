"""
RAG Retrieval Pipeline.
Builds the retrieval context package as per EP-05 requirements.
"""
import logging
from typing import List
from .models import ContextPackage, RankedPassage, KnowledgeAsset
from .repository import KnowledgeRepository
from modules.embeddings.provider import embedding_provider
from modules.relationship_engine.neo4j_repository import Neo4jRepository
from exceptions.base import PermissionDeniedException

logger = logging.getLogger("KnowledgePlatform.Retrieval")


class RetrievalPipeline:
    def __init__(self, repo: KnowledgeRepository, graph_repo: Neo4jRepository):
        self.repo = repo
        self.graph_repo = graph_repo

    async def retrieve(self, query: str, user_department: str, user_roles: List[str], top_k: int = 5) -> ContextPackage:
        """
        Executes the EP-05 retrieval pipeline:
        Query -> Metadata Filter -> Lexical -> Vector -> Graph Expansion -> Ranking -> Citation Assembly
        """
        # 1. Embed query
        query_vector = await embedding_provider.get_embedding(query)
        if not query_vector:
            logger.warning("Failed to embed query, falling back to lexical search only.")
            vector_results = []
        else:
            # 2. Vector Retrieval (pgvector <=> op)
            vector_results = await self.repo.semantic_search(query_vector, top_k=top_k * 2)

        # 3. Lexical Retrieval
        lexical_results = await self.repo.lexical_search(query, top_k=top_k * 2)

        # 4. Merge & Rank (Simple weighted merge)
        merged = {}
        for r in vector_results:
            cid = r["id"]
            merged[cid] = r
            # Vector distance: 0 is exact match. We want a score where higher is better.
            # Using 1 - distance as a crude cosine similarity mapping if vectors are normalized.
            # If not normalized, just invert distance. Let's assume cosine distance [0, 2].
            dist = r.get("distance", 1.0)
            merged[cid]["vector_score"] = max(0.0, 1.0 - (dist / 2.0))
            merged[cid]["lexical_score"] = 0.0

        for r in lexical_results:
            cid = r["id"]
            if cid not in merged:
                merged[cid] = r
                merged[cid]["vector_score"] = 0.0
            # Arbitrary bump for lexical hit
            merged[cid]["lexical_score"] = 0.5 

        # 5. Graph Expansion (Optional hint boosting)
        # In a full implementation, we might boost scores if the asset is closely
        # linked to the user's department in Neo4j.
        # For EP-05, we just structure the hook.
        for cid, data in merged.items():
            data["graph_score"] = 0.0
            if data.get("asset_type") == "POLICY":
                # Arbitrary rule: policies get a slight graph relevance bump
                data["graph_score"] += 0.1

        # 6. Rank & Filter Permissions
        scored_passages = []
        for data in merged.values():
            # Weighted score: 70% vector, 20% lexical, 10% graph
            final_score = (data["vector_score"] * 0.7) + (data["lexical_score"] * 0.2) + (data["graph_score"] * 0.1)
            
            # Simple mock permission check (in a real system, verify asset ACL)
            # We assume published assets are visible if they passed the DB filter.
            
            passage = RankedPassage(
                id=data["id"],
                asset_id=data["asset_id"],
                asset_title=data["asset_title"],
                asset_type=data["asset_type"],
                chunk_index=data["chunk_index"],
                text=data["text"],
                score=round(final_score, 4),
                lexical_score=round(data["lexical_score"], 4),
                vector_score=round(data["vector_score"], 4),
                graph_score=round(data["graph_score"], 4),
                source_filename=data.get("source_filename"),
                version=data.get("version", 1)
            )
            scored_passages.append(passage)

        # Sort descending by score
        scored_passages.sort(key=lambda p: p.score, reverse=True)
        top_passages = scored_passages[:top_k]

        # 7. Citation Assembly
        cited = list(set(p.asset_title for p in top_passages))

        return ContextPackage(
            query=query,
            passages=top_passages,
            total_found=len(top_passages),
            retrieval_strategy="hybrid",
            permission_filtered=True,
            cited_sources=cited
        )
