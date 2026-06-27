import asyncio
import logging
from modules.rag.engine import RAGEngine
from modules.knowledge_index.collections import KnowledgeCollection

logging.basicConfig(level=logging.DEBUG)

async def test_rag():
    engine = RAGEngine()
    
    print("Executing RAG Pipeline for a Level 1 User in the Steel Melting Shop...")
    
    # The mock returns 2 documents:
    # 1. EAF doc (Level 1, STEEL_MELTING_SHOP)
    # 2. HR doc (Level 5, HR)
    
    context = await engine.get_ai_context(
        query="What temperature does the EAF run at?",
        collection=KnowledgeCollection.MANUFACTURING,
        user_department="STEEL_MELTING_SHOP",
        user_roles=["operator"],
        user_clearance=1
    )
    
    print("\n--- Context Package Formatted Output ---")
    print(context.format_for_prompt())
    print("\n--- Summary ---")
    print(f"Total Found: {context.total_found}")
    print(f"Related Resources: {context.related_resources}")

if __name__ == "__main__":
    asyncio.run(test_rag())
