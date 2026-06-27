# AI Context Manager & Intelligent Routing Architecture

## Overview
Implementation Plan 4.2 establishes the middle-tier routing logic for the JSL Contingency Learning Platform's AI implementation. Rather than allowing frontend requests to directly hit the `EnterpriseAIGateway`, all requests must first traverse the `IntelligentRouter`.

## The Routing Pipeline

1. **Request Intake (`AIRequestPayload`)**
   - The user submits a raw query. The frontend intercepts this query and attaches positional metadata (e.g., `current_url`, `module_context_id`).

2. **Persona Evaluation (`AIPersona`)**
   - The router analyzes the `current_url` and query keywords. If the user is on an equipment page, the `MANUFACTURING_EXPERT` persona is assigned. If the query involves "hazard", the `SAFETY_EXPERT` is assigned. This dictates the system tone and priorities.

3. **Context Gathering (`ContextResolution`)**
   - The `ContextManager` uses the user's ID to fetch internal permissions, current department state, and the precise ID of the lesson or SOP currently being viewed.

4. **Prompt Compilation (`PromptEngine`)**
   - The `PromptEngine` securely formats the extracted context and the persona tone *before* appending the raw user query, preventing malicious prompt injection attacks.

5. **Gateway Execution (`EnterpriseAIGateway`)**
   - Finally, the gateway receives the sanitized prompt, runs a final permission check (verifying the user is actually authorized to query the compiled context), executes the request against Ollama, and logs the Token/Latency audit trail.

## Future Integration Hooks
- **RAG/Knowledge Base**: Stage 4.3+ will hook into the `ContextManager` to inject `document_chunks` alongside the `current_lesson_id`.
- **SAP**: The ContextManager is designed to eventually pull Live SCADA/SAP metrics into the prompt context if the `AITaskType` resolves to `EQUIPMENT_EXPLANATION`.
