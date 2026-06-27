import logging
from modules.ai_orchestrator.engine import OrchestratorEngine

logging.basicConfig(level=logging.DEBUG)

def test_orchestrator():
    print("--- Testing Enterprise AI Orchestrator ---")
    
    engine = OrchestratorEngine()
    
    # Simulate a complex multi-intent query
    query = "What is the max equipment spec for the EAF and what are the safety hazards?"
    
    print("\n--- Sending Query to Orchestrator ---")
    final_payload = engine.process_request(query)
    
    print("\n--- Final Aggregated Response ---")
    print(final_payload["final_answer"])
    
    print(f"\nAgents Used: {final_payload['agents_used']}")
    print(f"Merged Sources: {final_payload['merged_sources']}")
    
    print("\nTest Complete!")

if __name__ == "__main__":
    test_orchestrator()
