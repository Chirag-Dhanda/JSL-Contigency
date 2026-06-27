# Enterprise Architecture

## 1. Overall System Architecture
The JSL Contingency Platform is a monolithic backend with a modular domain-driven design, paired with a React frontend. It acts as an intelligent middleware layer integrating standard enterprise operations (Auth, HR, Manufacturing) with advanced local AI capabilities (Ollama, ChromaDB).

## 2. Frontend Architecture
- **Framework**: React (Vite)
- **Styling**: Vanilla CSS with modern, dark-themed aesthetics.
- **Key Dashboards**: 
  - Performance Monitoring
  - AI Orchestrator UI
  - Unified System Health

## 3. Backend Architecture
- **Framework**: FastAPI (Python)
- **Dependency Injection**: Custom `Container` class (`core.di`) for service management.
- **Modularity**: Domain-driven structure in `backend/modules/`. Each module is self-contained.
- **Lifecycle Management**: `core.lifecycle` handles module registration, initialization, and clean shutdown.

## 4. Authentication Architecture
- **Core Mechanism**: JWT-based stateless authentication.
- **RBAC**: Role-Based Access Control via the `permissions` module.
- **DBAC**: Department-Based Access Control via the `authorization` module.
- **Temporary Access**: The `access_request` module handles time-bound elevation of privileges.

## 5. AI Platform Architecture
- **Entry Point**: `EnterpriseAIGateway` enforces security and blocks restricted queries.
- **Context Engine**: Injects implicit user state (Role, Department, Current View).
- **Runtime**: `IntelligentCache` and `RequestQueue` protect the LLM from overload.
- **Orchestrator**: A Multi-Agent system that routes queries to specialized domain experts (`MfgExpert`, `SafetyExpert`, etc.).

## 6. Learning Platform
- **Roadmap Engine**: A Directed Acyclic Graph (DAG) managing employee onboarding journeys.
- **Nodes**: Welcome videos, Safety lessons, Department overviews.
- **Progression**: Strict dependencies lock future stages until prerequisites are met.

## 7. Knowledge Platform & RAG Architecture
- **Ingestion**: Documents are authored via `KnowledgeService`.
- **Storage**: Vectorized using `nomic-embed-text` and stored in ChromaDB collections (`KnowledgeIndex`).
- **Retrieval**: Agents perform similarity searches to retrieve enterprise context before generating answers.

## 8. Database Architecture
- **Relational Data**: (Mocked/In-Memory for Stage 4) Users, Roles, Events, Audit Logs.
- **Vector Data**: Local ChromaDB instance managing high-dimensional semantic search.

## 9. Communication Flow
- **Event Bus**: The `events` module acts as a Pub/Sub hub (`DomainEvent`).
- **Notifications**: Subsystems (like `Auth`) publish events (`USER_REGISTERED`) which the Notification Service catches and processes using the `templates` engine.

## 10. Module Relationships
Modules are designed to be loosely coupled, communicating primarily via Dependency Injection and the Event Bus to prevent circular dependencies.
