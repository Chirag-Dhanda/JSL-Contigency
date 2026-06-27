import sys
import asyncio
from modules.vector_db.module import VectorDBModule
from modules.vector_db.health import health_service

async def verify():
    print("--- Starting ChromaDB Verification ---")
    module = VectorDBModule()
    
    try:
        await module.initialize()
        print("SUCCESS: ChromaDB Initialized successfully.")
    except Exception as e:
        print(f"FAILED: Initialization Failed: {e}")
        sys.exit(1)
        
    health = health_service.check_health()
    print("--- Health Check Results ---")
    print(health)
    
    if health["status"] == "healthy":
        print("SUCCESS: Health check passed.")
    else:
        print("FAILED: Health check failed.")
        sys.exit(1)
        
    print("--- Verification Complete ---")

if __name__ == "__main__":
    asyncio.run(verify())
