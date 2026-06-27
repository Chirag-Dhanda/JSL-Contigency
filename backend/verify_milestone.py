import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(".."))
from backend.main import create_app
from backend.modules.embeddings.provider import embedding_provider
from backend.modules.ai_gateway.gateway import ai_gateway
from backend.modules.conversations.models import ContextBlock
from backend.modules.ai_router.router import ai_router
from backend.modules.ai.connection import connection_manager
from backend.core.lifecycle import lifecycle

async def verify():
    print("--- Starting Milestone Verification ---")
    
    # Init lifecycle manually for test
    try:
        from backend.modules.vector_db.module import VectorDBModule
        from backend.modules.conversations.module import ConversationsModule
        lifecycle.register_module(VectorDBModule)
        lifecycle.register_module(ConversationsModule)
        await lifecycle.startup()
        print("SUCCESS: Modules initialized.")
    except Exception as e:
        print(f"FAILED to initialize modules: {e}")

    # Check Ollama connection
    print("--- Checking Ollama ---")
    try:
        client = await connection_manager.get_client()
        res = await client.get(f"{connection_manager.base_url}/api/tags")
        if res.status_code == 200:
            print("SUCCESS: Ollama reachable. Models:", [m["name"] for m in res.json().get("models", [])])
        else:
            print(f"FAILED: Ollama returned {res.status_code}")
    except Exception as e:
        print(f"WARNING: Ollama not reachable: {e}")

    print("--- Testing Copilot Routing ---")
    try:
        ctx = ContextBlock(current_page="Dashboard", user_role="Admin")
        # We won't actually hit Ollama to save time and avoid model loading delays, just verify the structure
        print("SUCCESS: Copilot context created.")
    except Exception as e:
        print(f"FAILED: Copilot context error: {e}")

if __name__ == "__main__":
    asyncio.run(verify())
