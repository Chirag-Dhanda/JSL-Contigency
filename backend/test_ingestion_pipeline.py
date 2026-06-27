import asyncio
import logging
from modules.ingestion.engine import IngestionEngine
from modules.document_processing.parsers import PDFParser
from modules.document_processing.metadata import MetadataExtractor
from modules.chunking.engine import ChunkingEngine
from modules.indexing.pipeline import IndexingPipeline
from modules.knowledge_index.collections import KnowledgeCollection

logging.basicConfig(level=logging.DEBUG)

async def test_ingestion():
    # 1. Ingestion & Validation
    ingestion = IngestionEngine()
    print("--- 1. Ingestion & Validation ---")
    job_id = ingestion.receive_upload("C:/mock/data/sms_eaf_manual.pdf", "STEEL_MELTING_SHOP")
    
    print("\n--- 2. Parsing & Cleaning ---")
    parser = PDFParser()
    cleaned_text = parser.parse("C:/mock/data/sms_eaf_manual.pdf")
    print(f"Cleaned Text Output: '{cleaned_text}'")
    
    print("\n--- 3. Metadata Extraction ---")
    extractor = MetadataExtractor()
    meta = extractor.extract("C:/mock/data/sms_eaf_manual.pdf", "STEEL_MELTING_SHOP")
    print(f"Extracted Metadata Role Access: {meta.role_access}")
    
    print("\n--- 4. Chunking ---")
    chunker = ChunkingEngine(chunk_size=5, overlap=1)
    chunks = chunker.chunk_document(cleaned_text, meta)
    print(f"Total Chunks Generated: {len(chunks)}")
    for c in chunks:
        print(f"Chunk {c.chunk_index}: '{c.text}'")
        
    print("\n--- 5. Indexing ---")
    indexer = IndexingPipeline()
    await indexer.index_document(chunks, KnowledgeCollection.MANUFACTURING)
    
    print("\nPipeline Complete!")

if __name__ == "__main__":
    asyncio.run(test_ingestion())
