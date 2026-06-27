# Enterprise AI Architecture

This document defines the high-level architecture of the Enterprise AI Platform (Stage 4 Baseline).

## Core Philosophy
The platform acts as a secure, scalable, and intelligent middleware between enterprise users and localized LLM inference engines (Ollama) and Vector Databases (ChromaDB).

## System Components

### 1. Security & Routing Layer
- **EnterpriseAIGateway**: The front-door for all AI requests. Evaluates safety policies and restricts access before any LLM processing occurs.
- **ContextManager**: Resolves implicit context (who is the user, what role do they have, what screen are they looking at).
- **PermissionValidator**: Hard-enforces whether a user has the explicit RBAC rights to ask a query.

### 2. Runtime Engine (Performance & Resilience)
- **IntelligentCache**: Hashes requests. If an identical semantic request is found, it bypasses the LLM and serves the answer instantly.
- **RequestQueue**: Enforces concurrent backpressure limits to prevent LLM OOM crashes.
- **CircuitBreaker**: Fails-fast if a downstream service (like Ollama) goes offline.

### 3. Execution & Orchestration
- **OrchestratorEngine**: The task planner. It takes a query and delegates it to specialized agents.
- **Agent Registry**: Maintains the active specialized agents:
  - `MfgExpert`: For industrial equipment and specifications.
  - `SOPExpert`: For Standard Operating Procedures and safety guidelines.
  - `LearningMentor`: For adaptive training and onboarding.

### 4. Infrastructure Layer
- **Ollama Client**: Local LLM execution.
- **ChromaDB**: Local vector storage for RAG (Retrieval-Augmented Generation).
- **PromptStudio**: Centralized prompt templates.
