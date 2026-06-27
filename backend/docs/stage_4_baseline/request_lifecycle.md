# Request Lifecycle

Every AI request entering the Enterprise AI Platform strictly follows this synchronous lifecycle:

1. **User Action**: The user submits a query via the Frontend Copilot.
2. **Gateway Interception**: The `EnterpriseAIGateway` intercepts the request. It scans for restricted keywords (e.g., "password", "salary") and blocks if necessary.
3. **Context Resolution**: The `ContextManager` attaches implicit state to the request (e.g., "User is currently viewing the EAF dashboard").
4. **Permission Check**: The `PermissionValidator` confirms the user's role allows AI queries.
5. **Caching**: The `IntelligentCache` (within the `RuntimeEngine`) checks if this exact query was answered recently. If yes, it returns immediately (0ms LLM latency).
6. **Queuing**: If not cached, the request enters the `RequestQueue`. If the system is over capacity, it fails-fast.
7. **Prompt Construction**: The `PromptEngine` retrieves the approved system template.
8. **Orchestration**: The `OrchestratorEngine` parses the query, identifies required capabilities, and routes the query to the correct Agent (e.g., `MfgExpert`).
9. **RAG Execution**: The Agent queries ChromaDB, retrieves enterprise knowledge, and formulates an answer via Ollama.
10. **Aggregation**: The orchestrator merges agent responses.
11. **Caching & Return**: The response is saved to the cache and streamed back to the frontend.
