import logging
from typing import List

from modules.rag.models import AIContextPackage, RetrievedPassage
from modules.retrieval.pipeline import RetrievalPipeline
from modules.knowledge_index.collections import KnowledgeCollection
from modules.knowledge_index.metadata import DocumentMetadata

logger = logging.getLogger("RAGEngine")

class RAGEngine:
    """The public API for the RAG platform. Used by the AI Router."""
    
    def __init__(self):
        self.retrieval_pipeline = RetrievalPipeline()
        
    async def get_ai_context(self, 
                             query: str, 
                             collection: KnowledgeCollection,
                             user_department: str,
                             user_roles: List[str],
                             user_clearance: int) -> AIContextPackage:
        """
        Executes a retrieval and packages it neatly for the Prompt Engine.
        """
        logger.info("RAGEngine preparing AI context...")
        
        raw_results = await self.retrieval_pipeline.execute_retrieval(
            query=query,
            collection=collection,
            user_department=user_department,
            user_roles=user_roles,
            user_clearance_level=user_clearance,
            top_k=3
        )
        
        passages = []
        related_sources = []
        
        for r in raw_results:
            meta = DocumentMetadata(**r["metadata"])
            passages.append(
                RetrievedPassage(
                    id=r["id"],
                    text=r["text"],
                    score=r["score"],
                    metadata=meta
                )
            )
            if meta.document_source not in related_sources:
                related_sources.append(meta.document_source)
                
        package = AIContextPackage(
            passages=passages,
            collection_searched=collection.value,
            total_found=len(passages),
            related_resources=related_sources
        )
        
        return package
