import logging
from modules.manufacturing_ai.engine import ManufacturingAIEngine

logging.basicConfig(level=logging.DEBUG)

def test_manufacturing_ai():
    print("--- Testing Manufacturing AI Engine ---")
    engine = ManufacturingAIEngine()
    
    # Query 1: Troubleshooting the EAF
    query_1 = "Why is the Electric Arc Furnace temperature dropping rapidly?"
    user_context = {"role": "Engineer"}
    
    response_1 = engine.process_query(query_1, user_context)
    
    print("\n--- Query 1 Results ---")
    print(f"Expert Selected: {response_1.expert_used}")
    print(f"Answer: {response_1.answer}")
    print(f"Confidence: {response_1.confidence}")
    print(f"Related SOPs Cited: {response_1.related_sops}")

    # Query 2: Safety Guidance
    query_2 = "What PPE is required for the rolling mill?"
    
    response_2 = engine.process_query(query_2, user_context)
    
    print("\n--- Query 2 Results ---")
    print(f"Expert Selected: {response_2.expert_used}")
    print(f"Confidence: {response_2.confidence}")
    
    print("\nTest Complete!")

if __name__ == "__main__":
    test_manufacturing_ai()
