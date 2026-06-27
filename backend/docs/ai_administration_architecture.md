# Enterprise AI Administration, Governance & Model Management

## Overview
Implementation Plan 4.11 establishes a centralized control center for the Enterprise AI ecosystem. Because this platform utilizes generative AI across sensitive industrial workflows, strict governance, auditing, and health monitoring are non-negotiable architectural requirements.

## 1. Model Management (`modules/model_management`)
The `AdminModelManager` tracks the local models (like `llama3` for chat and `nomic-embed-text` for vectorization).
- **`AIModelConfig`**: A rigid schema allowing admins to configure `temperature`, `top_p`, `max_tokens`, and `context_length`. This ensures that safety experts don't hallucinate (by forcing low temperature) while creative tasks might use higher thresholds.
- Admins can hot-swap the default chat model or completely disable a rogue model.

## 2. AI Security & Governance (`modules/ai_security` & `modules/ai_admin`)
- **`AIPermissionManager`**: Enforces Role-Based Access Control (RBAC). It explicitly restricts which roles can talk to which AI Agents (e.g., an entry-level operator cannot query the HR Data Agent).
- **`AIAuditLogger`**: The most critical governance component. Every single AI request across the platform is logged here. It strictly records the `user_id`, `timestamp`, `question`, the exact `model_used`, and crucially, the `knowledge_sources_used` (SOPs, Lessons). If an operator acts on bad AI advice, the audit log will definitively prove which document the AI hallucinated from.
- **`PromptGovernance`**: Version controls the system prompts that dictate the behavior of our agents.

## 3. Monitoring & Analytics (`modules/ai_monitoring`)
- **`HealthMonitor` & `AlertSystem`**: Periodically pings the Enterprise Gateway, Ollama service, and ChromaDB vector database. If a service goes offline, or if the vector DB storage exceeds 85%, it flags an alert to prevent silent failures.
- **`UsageAnalytics`**: Rolls up the Audit Logs into metrics like `daily_requests`, `average_response_time_ms`, and `failure_rate_percent`.

## 4. Frontend Integration
The `AdminDashboard.jsx` acts as the single pane of glass. It consumes the backend data to render three primary widgets:
1. **System Health**: A live view of service statuses and a visual progress bar for Vector Storage Usage.
2. **Usage Analytics**: High-level telemetry for the past 24 hours.
3. **Active Models**: A list of currently installed LLMs, their capabilities (e.g., `embeddings`, `chat`), and visual indicators showing if they are enabled or set as the default model.
