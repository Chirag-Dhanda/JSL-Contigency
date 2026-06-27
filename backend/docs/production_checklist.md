# Enterprise Production Readiness Checklist

Before the AI Platform goes live in the manufacturing environment, the following configurations and fail-safes must be validated:

## 1. Runtime Configurations
- [ ] `max_concurrent_requests` matches the hardware capacity of the host node.
- [ ] `max_queue_size` is configured to prevent excessive wait times (e.g., 20).
- [ ] `cache_ttl_seconds` is configured appropriately (e.g., 3600s for standard queries).

## 2. Fault Tolerance Checks
- [ ] Circuit Breaker `failure_threshold` is set (e.g., 3 failures).
- [ ] Circuit Breaker `reset_timeout` allows sufficient time for service recovery (e.g., 60 seconds).
- [ ] Graceful degradation messages are verified for "Server Overloaded" and "Service Offline" states.

## 3. Security & Governance (Verification of Prior Plans)
- [ ] Audit Logger is confirmed writing to permanent storage.
- [ ] Permission Manager is actively blocking unauthorized agent access.
- [ ] System Prompts are locked in the `PUBLISHED` state via the Prompt Studio.

## 4. Observability
- [ ] Performance Dashboard is successfully retrieving live Cache Hit Rates.
- [ ] System Health Dashboard is actively pinging Ollama and ChromaDB.
