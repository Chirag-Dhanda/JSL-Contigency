import asyncio
import logging
from modules.ai_router.router import IntelligentRouter
from modules.ai_router.models import AIRequestPayload

logging.basicConfig(level=logging.DEBUG)

def test_router():
    router = IntelligentRouter()
    
    # Simulate a user asking about a hazard while on a safety page
    payload = AIRequestPayload(
        user_id="usr-123",
        query="What should I do if the alarm goes off?",
        current_url="https://jsl-contingency.local/safety/fire"
    )
    
    print("Sending Request to Router...")
    response = router.route_request(payload)
    
    print("\n--- Router Response ---")
    print(f"Answer: {response.answer}")
    print(f"Persona Selected: {response.metadata.persona_used}")
    print(f"Latency: {response.metadata.latency_ms}ms")

if __name__ == "__main__":
    test_router()
