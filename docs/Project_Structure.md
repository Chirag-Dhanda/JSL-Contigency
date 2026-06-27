# Project Structure

The JSL Contingency platform enforces strict domain-driven modularity.

## `backend/` (FastAPI Server)
- **`core/`**: The backbone of the application.
  - `di/`: Custom Dependency Injection container.
  - `lifecycle/`: Module registration and startup sequences.
- **`exceptions/`**: Global exception classes (`base.py`) for consistent error handling.

## `backend/modules/` (Domain Modules)
This directory contains over 80 specific domain modules. Key modules include:

### Enterprise AI Core
- **`ai_gateway/`**: The `EnterpriseAIGateway` (Security & Audit).
- **`ai_integration/`**: Contains `facade.py`, the master entry point unifying all AI services.
- **`ai_runtime/`**: Queuing and backpressure management.
- **`ai_orchestrator/`**: The multi-agent task planner and executor.
- **`ai_cache/`**: Intelligent semantic caching to save LLM compute.
- **`agents/`**: The specialized `BaseAgent` implementations (Mfg, Safety).
- **`prompts/` & `prompt_studio/`**: Centralized prompt template management.
- **`vector_db/`**: ChromaDB integration logic.

### Enterprise Identity & Security
- **`auth/`**: JWT login, logout, password resets.
- **`permissions/`**: RBAC (Role-Based Access Control) engine.
- **`authorization/`**: DBAC (Department-Based Access Control) pipeline.
- **`access_request/`**: Temporary privilege elevation workflow.

### Enterprise Knowledge & Operations
- **`knowledge/`**: Document ingestion and lifecycle management.
- **`manufacturing/`**: Factory digital twin logic (Stations, Work Centers).
- **`roadmap/`**: Employee training DAG (Directed Acyclic Graph) progression.
- **`events/` & `notifications/`**: Internal Pub/Sub bus and notification templates.

## `frontend_app/` (React SPA)
- **`src/components/`**: The UI widgets.
  - `UnifiedHealthDashboard.jsx`: Master system monitor.
  - `OrchestratorDashboard.jsx`: AI Agent execution visualizer.
  - `PerformanceDashboard.jsx`: Cache hit rate and latency monitor.
- **`src/App.jsx`**: The main application routing and state container.
