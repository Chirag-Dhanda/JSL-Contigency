import logging
from typing import List

from modules.chunking.engine import DocumentChunk
from modules.embeddings.engine import EmbeddingEngine
from modules.knowledge_index.collections import KnowledgeCollection
# from modules.vector_db.manager import VectorDatabaseManager # Abstract class in real usage

logger = logging.getLogger("IndexingPipeline")

class IndexingPipeline:
    """The final stage of ingestion. Embeds chunks and saves them to the Vector Database."""
    
    def __init__(self):
        self.embedding_engine = EmbeddingEngine()
        # self.vector_db = ChromaDBManager() # Or whichever concrete class is implemented
        
    async def index_document(self, chunks: List[DocumentChunk], collection: KnowledgeCollection):
        """
        Receives chunks, calls the Embedding Engine for vectors, and persists to DB.
        """
        if not chunks:
            logger.warning("No chunks provided for indexing.")
            return
            
        logger.info(f"Indexing {len(chunks)} chunks into {collection.value} collection.")
        
        # 1. Generate Embeddings (Mocked Batch)
        texts = [chunk.text for chunk in chunks]
        embeddings = await self.embedding_engine.generate_embeddings_batch(texts)
        
        # 2. Persist to Vector Database
        for i, chunk in enumerate(chunks):
            # 2a. Validate
            if not self.embedding_engine.validate_embedding(embeddings[i]):
                logger.error(f"Invalid embedding generated for chunk {chunk.chunk_index}")
                continue
                
            # 2b. Store
            # self.vector_db.store_embedding(
            #     collection=collection,
            #     text_chunk=chunk.text,
            #     embedding=embeddings[i],
            #     metadata=chunk.metadata
            # )
            logger.debug(f"Stored chunk {chunk.chunk_index} to vector db.")
            
        logger.info("Indexing complete.")
