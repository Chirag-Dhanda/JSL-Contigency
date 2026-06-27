import logging
from modules.ai_runtime.engine import RuntimeEngine
from modules.resilience.circuit_breaker import CircuitBreaker
from modules.performance.load_tester import LoadTestFramework
import time

logging.basicConfig(level=logging.DEBUG)

def test_runtime():
    print("--- Testing Enterprise AI Runtime & Optimization ---")
    
    engine = RuntimeEngine()
    
    # 1. Test Smart Caching
    print("\n--- 1. Testing Smart Caching ---")
    query = "What is the EAF safety protocol?"
    
    print("First Request (Cache Miss):")
    res1 = engine.submit_request(query)
    print(f"Status: {res1['status']} | Source: {res1.get('source')}")
    
    print("\nSecond Request (Cache Hit):")
    res2 = engine.submit_request(query)
    print(f"Status: {res2['status']} | Source: {res2.get('source')}")
    
    metrics = engine.metrics.get_metrics_snapshot()
    print(f"Cache Hit Rate: {metrics['cache_hit_rate_percent']}%")
    
    # 2. Test Concurrency & Queuing (Backpressure)
    print("\n--- 2. Testing Queue & Backpressure ---")
    tester = LoadTestFramework()
    
    # Force the engine active requests to limit to simulate load
    engine.active_requests = engine.config.max_concurrent_requests
    
    # Max queue size is 20. If we submit 25, 20 should queue, 5 should reject.
    load_results = tester.simulate_concurrent_requests(engine, 25)
    
    print(f"Queue Load Results: {load_results}")
    print(f"Current Queue Depth: {engine.queue.get_depth()}")
    
    # 3. Test Circuit Breaker
    print("\n--- 3. Testing Circuit Breaker ---")
    breaker = CircuitBreaker(failure_threshold=2, reset_timeout_seconds=2)
    
    print(f"Initial Status (Safe?): {breaker.check_status()}")
    breaker.record_failure()
    print(f"After 1 failure (Safe?): {breaker.check_status()}")
    breaker.record_failure()
    print(f"After 2 failures (Safe?): {breaker.check_status()}")
    
    print("Waiting 3 seconds for timeout...")
    time.sleep(3)
    print(f"After timeout (Safe?): {breaker.check_status()}")
    
    print("\nTest Complete!")

if __name__ == "__main__":
    test_runtime()
