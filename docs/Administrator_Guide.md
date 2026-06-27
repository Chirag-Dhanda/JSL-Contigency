# Administrator Guide

This guide is intended for system administrators managing the JSL Contingency Enterprise Platform.

## 1. System Configuration & Monitoring
The primary tool for system administrators is the **Unified Health Dashboard**, accessible via the main frontend navigation. 

### Core Services
- Ensure the `Frontend App`, `Backend API`, and `Enterprise Gateway` remain "Online".
- If the Gateway is offline, no AI queries can be processed, as it enforces the central security policies.

### Inference & Embeddings
- The system depends on local inference to maintain data sovereignty. 
- Ensure `Ollama Local` and `ChromaDB Vector` remain "Online".
- If Ollama goes offline, the Circuit Breaker will trip to prevent cascading timeouts.

### Runtime & Orchestration
- Keep an eye on the `Agent_Registry` status. If an agent (e.g., `MfgExpert`) drops offline, queries regarding manufacturing specs will fail to resolve.

## 2. Managing Users & Roles
- **RBAC**: Users are assigned roles (e.g., Admin, Engineer). Roles are tied to explicit permissions (`models.py` in the `permissions` module).
- **DBAC**: Department-based access control prevents users in one department (e.g., Sales) from viewing resources in another (e.g., Finance) without a Temporary Access Request.
- **Temporary Access**: Administrators can approve access requests in the `access_request` module, granting elevated privileges for a limited time (e.g., 60 minutes).

## 3. Managing AI Prompts
Do not edit code to change the AI's behavior. Use the **Prompt Studio** module.
- AI system templates (e.g., the safety constraint prompt) can be managed via the `modules/prompt_studio`.
- This ensures a centralized, version-controlled repository of enterprise AI instructions.

## 4. Managing Knowledge (SOPs & Learning Content)
- Use the `KnowledgeService` (`modules/knowledge`) to author new content.
- Content exists in Draft (`ContentStatus.DRAFT`) until explicitly published by an administrator.
- The `Knowledge Pipeline` automatically handles OCR, parsing, chunking, and embedding into ChromaDB upon publication.

## 5. Managing Certificates & Roadmap
- The **Roadmap Engine** dictates employee training journeys. Nodes (Lessons, Videos) are locked until prerequisites are met.
- Administrators can define these DAGs (Directed Acyclic Graphs) in the `roadmap` module.
