# AI Architecture Guide

The AI architecture is designed for enterprise-grade security, scalability, and domain specificity.

## 1. Enterprise AI Gateway
The gatekeeper. It intercepts all AI traffic.
- **Security Check**: Blocks restricted queries (e.g., "what is the CEO's salary").
- **Audit Logging**: Logs the user, prompt, model, and latency for compliance.

## 2. Context Manager
Instead of forcing the user to type long prompts, the `ContextManager` implicitly injects the user's state. If a user asks "What is the pressure limit?", the Context Manager appends "The user is currently viewing the EAF-01 dashboard" to the query.

## 3. Prompt Engine & Prompt Studio
All system instructions are decoupled from business logic. The `PromptEngine` retrieves centrally managed prompt templates, ensuring consistency in how the AI behaves across the enterprise.

## 4. Runtime (Cache & Queue)
To protect the local LLM from Out-Of-Memory (OOM) crashes:
- **IntelligentCache**: Hashes the incoming query. If a semantic match exists, it serves the cached response instantly.
- **RequestQueue**: Implements backpressure. If concurrent requests exceed the limit, it rejects the request gracefully rather than crashing the server.

## 5. Multi-Agent Orchestrator
The `OrchestratorEngine` parses a complex user query and splits it into a task graph. It then dispatches tasks to the appropriate domain agents in the `AgentRegistry`.
- **Manufacturing Expert (`MfgExpert`)**: Specialized in equipment specs and telemetry.
- **SOP Expert (`SafetyExpert`)**: Specialized in LOTO procedures and safety guidelines. Crucially instructed to NEVER hallucinate procedures.
- **Learning Mentor**: Specialized in recommending training modules based on the employee's `roadmap` progress.

## 6. Enterprise RAG Pipeline (ChromaDB)
Retrieval-Augmented Generation.
- When an agent needs information, it queries the `EmbeddingPipeline` (using `nomic-embed-text`).
- It performs a similarity search against the enterprise `ChromaDB`.
- The retrieved knowledge is injected into the LLM context window.

## 7. Ollama (Qwen / Llama3)
The execution engine. We run inference locally to ensure no proprietary enterprise data leaves the secure network.
