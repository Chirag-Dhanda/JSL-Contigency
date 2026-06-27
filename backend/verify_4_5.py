import sys
import asyncio
from modules.vector_db.module import VectorDBModule
from modules.embeddings.module import EmbeddingsModule
from modules.index_management.module import IndexManagementModule
from modules.synchronization.module import SynchronizationModule

from modules.embeddings.provider import embedding_provider
from modules.embeddings.engine import embedding_engine

async def verify():
    print("--- Starting 4.5 Verification ---")
    
    vec_db = VectorDBModule()
    emb_mod = EmbeddingsModule()
    idx_mod = IndexManagementModule()
    sync_mod = SynchronizationModule()
    
    try:
        await vec_db.initialize()
        await idx_mod.initialize()
        await emb_mod.initialize()
        await sync_mod.initialize()
        print("SUCCESS: All modules initialized successfully.")
    except Exception as e:
        print(f"FAILED: Initialization Failed: {e}")
        sys.exit(1)
        
    print("--- Embedding Engine Status ---")
    print(f"Model Name: {embedding_provider.model_name}")
    print(f"Queue Status: {embedding_engine.stats}")
    
    print("--- Health Checks ---")
    provider_health = await embedding_provider.check_health()
    if provider_health:
        print("SUCCESS: Embedding provider detected successfully.")
    else:
        print("WARNING: Embedding model not detected locally in Ollama (expected if Ollama is not running or model is missing).")
        
    await emb_mod.shutdown()
    
    print("--- Verification Complete ---")

if __name__ == "__main__":
    asyncio.run(verify())
