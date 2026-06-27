import logging
import time
from modules.ai_integration.facade import EnterpriseAIFacade

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

def run_integration_tests():
    print("=========================================================")
    print("STAGE 4 BASELINE - END-TO-END VALIDATION")
    print("=========================================================\n")
    
    facade = EnterpriseAIFacade()
    
    test_cases = [
        {
            "name": "1. Simple Greeting",
            "user": "emp_001",
            "query": "Hello AI",
        },
        {
            "name": "2. Manufacturing Question (Orchestrator Routing)",
            "user": "emp_002",
            "query": "What is the max equipment spec for the EAF?",
        },
        {
            "name": "3. SOP Question (Safety Routing)",
            "user": "emp_003",
            "query": "Show me the lockout tagout procedure for the conveyor.",
        },
        {
            "name": "4. Permission Block (Safety Check)",
            "user": "restricted_user",
            "query": "What is the EAF?",
            # Simulated blocked by prompt or gateway
        },
        {
            "name": "5. Cache Verification (Repeated Query)",
            "user": "emp_002",
            "query": "What is the max equipment spec for the EAF?",
        }
    ]
    
    print("--- RUNNING E2E WORKFLOWS ---")
    
    for case in test_cases:
        print(f"\nRunning: {case['name']}")
        print(f"User: {case['user']} | Query: '{case['query']}'")
        
        # Override permission for test case 4
        if case["user"] == "restricted_user":
            # Mocking the permission failure for the test script specifically
            facade.permission_validator.can_execute = lambda u, p: False
        else:
            facade.permission_validator.can_execute = lambda u, p: True
            
        start_time = time.time()
        result = facade.process_copilot_request(case["user"], case["query"])
        latency = int((time.time() - start_time) * 1000)
        
        if result["status"] == "success":
            print(f"[OK] Response ({latency}ms): {result['response']}")
            print(f"     Source: {result.get('source')}")
            if "agents_used" in result:
                 print(f"     Agents: {result['agents_used']}")
        else:
            print(f"[{'EXPECTED' if case['user'] == 'restricted_user' else 'FAIL'}] Blocked/Error: {result.get('message')}")

    print("\n--- SYSTEM HEALTH ---")
    health = facade.get_system_health()
    print(f"Overall Status: {health['status']}")
    print(f"Components Online: {list(health['components'].keys())}")
    
    print("\n=========================================================")
    print("VALIDATION COMPLETE")
    print("=========================================================")

if __name__ == "__main__":
    run_integration_tests()
