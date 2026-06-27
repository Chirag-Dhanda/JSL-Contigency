import sys
import os
import asyncio
sys.path.insert(0, os.path.abspath(".."))
from modules.conversations.module import ConversationsModule
from modules.conversations.models import ContextBlock
from modules.ai_router.router import ai_router

async def verify():
    print("--- Starting 4.6 Verification ---")
    
    conv_mod = ConversationsModule()
    
    try:
        await conv_mod.initialize()
        print("SUCCESS: Conversations Module initialized successfully.")
    except Exception as e:
        print(f"FAILED: Initialization Failed: {e}")
        sys.exit(1)
        
    print("--- Testing Context Block ---")
    try:
        ctx = ContextBlock(current_page="Equipment", current_equipment="Furnace-1", user_role="Manager")
        print(f"SUCCESS: Context Block structured properly: {ctx.model_dump()}")
    except Exception as e:
        print(f"FAILED: Context Block error: {e}")
        sys.exit(1)
        
    print("--- Testing AI Router Integration Methods ---")
    if hasattr(ai_router, 'route_copilot_request'):
        print("SUCCESS: AI Router supports Copilot Context injection.")
    else:
        print("FAILED: AI Router missing route_copilot_request.")
        sys.exit(1)

    print("--- Verification Complete ---")

if __name__ == "__main__":
    asyncio.run(verify())
