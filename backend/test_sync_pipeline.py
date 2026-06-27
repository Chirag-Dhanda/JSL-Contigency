import asyncio
import logging
from modules.synchronization.engine import SyncEngine
from modules.embeddings.provider import OllamaEmbeddingProvider
from modules.ai.config import ai_config

logging.basicConfig(level=logging.DEBUG)

async def test_sync_and_provider():
    print("--- 1. Testing Sync Engine ---")
    sync = SyncEngine()
    sync.synchronize()
    
    print("\n--- 2. Testing Ollama Embedding Provider ---")
    # Verify it reads from config correctly
    provider = OllamaEmbeddingProvider()
    print(f"Provider Model Configured: {provider.model}")
    print(f"Provider URL Configured: {provider.base_url}")
    
    # Check health (should fail gracefully if Ollama is not running)
    print("Checking Ollama Health...")
    is_healthy = await provider.check_health()
    print(f"Ollama Reachable: {is_healthy}")
    
    # Try embedding (with 1 retry for speed)
    print("\nAttempting to request embedding for 'Test String'...")
    embedding = await provider.get_embedding("Test String", retry_count=1)
    
    if embedding:
        print(f"Successfully generated embedding with dimension: {len(embedding)}")
    else:
        print("Embedding generation failed (expected if Ollama is offline). Process handled gracefully.")

if __name__ == "__main__":
    asyncio.run(test_sync_and_provider())
