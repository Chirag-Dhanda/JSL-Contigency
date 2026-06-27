from typing import List, Dict, Any, Optional
import abc

from modules.knowledge_index.metadata import DocumentMetadata
from modules.knowledge_index.collections import KnowledgeCollection

class VectorDatabaseManager(abc.ABC):
    """Abstract interface for local Vector Databases (e.g. ChromaDB, Qdrant)."""
    
    @abc.abstractmethod
    def create_collection(self, name: KnowledgeCollection):
        pass
        
    @abc.abstractmethod
    def store_embedding(self, 
                        collection: KnowledgeCollection, 
                        text_chunk: str, 
                        embedding: List[float], 
                        metadata: DocumentMetadata):
        pass

    @abc.abstractmethod
    def similarity_search(self, 
                          collection: KnowledgeCollection, 
                          query_embedding: List[float], 
                          top_k: int = 5) -> List[Dict[str, Any]]:
        pass
        
    @abc.abstractmethod
    def filtered_search(self, 
                        collection: KnowledgeCollection, 
                        query_embedding: List[float], 
                        filters: Dict[str, Any],
                        top_k: int = 5) -> List[Dict[str, Any]]:
        """Search incorporating strict metadata filtering."""
        pass

    @abc.abstractmethod
    def delete_document(self, collection: KnowledgeCollection, document_source_id: str):
        pass
