# Enterprise AI Platform Architecture

## Overview
The Enterprise AI Platform is designed to centralize and govern all AI interactions within JSL Contingency. It provides a robust, scalable foundation capable of interacting with local (Ollama) models and future cloud/SAP AI instances.

## Core Modules

### 1. AI Router (`backend/modules/ai_router`)
The AI Router acts as the intelligent middleware and primary entry point for all incoming requests before they reach the Gateway.
**Responsibilities:**
- Receiving AI Requests and mapping them to standard tasks (e.g., SOP Explanation, Lesson Guidance)
- Validating Permissions (e.g., clearance levels, module access limits)
- Selecting the appropriate AI Persona for the task
- Normalizing responses into a `StandardAIResponse` format

### 2. AI Gateway (`backend/modules/ai_gateway`)
The AI Gateway receives enriched context and persona definitions from the Router.
**Responsibilities:**
- Compiling Prompts via `PromptEngine` using provided Context and Personas
- Selecting Models via `ModelManager`
- Executing Requests and Handling Streaming
- Post Processing and Auditing

### 3. Context Manager (`backend/modules/context`)
Gathers comprehensive state information for prompt injection. Expanded to deeply resolve all environmental facets.
**Features:**
- Resolves User roles, departments, and clearance levels
- Resolves Active session parameters and current learning activities
- Gathers environment contexts (Manufacturing stage, active Equipment, active SOPs)

### 4. Prompt Engine & Personas (`backend/modules/prompts`)
Standardizes prompt construction across the application using configurable Personas.
**Features:**
- Configurable Personas (e.g., Manufacturing Expert, Safety Expert, Learning Mentor)
- Modular prompt templates (System, Role, Safety, Domain)
- Dynamic variable injection from `ContextManager`

### 5. Ollama Integration (`backend/modules/ai`)
Handles direct communication with local models via the Ollama API.
**Features:**
- Robust `ConnectionManager` with retry logic and exponential backoff
- Full streaming support for real-time AI responses
- Discovery of installed models
- Health checks for monitoring availability

### 6. Model Management (`backend/modules/model_management`)
Manages the lifecycle and availability of AI models.
**Features:**
- Auto-discovery of available models
- Graceful fallback strategies if default models are unavailable
- Capability detection (e.g., vision, tool-use)

### 7. Conversation Manager (`backend/modules/conversations`)
Maintains conversational state for contextual continuity.
**Features:**
- Session-based message tracking
- Metadata association for advanced analytics
- Automatic history formatting for context window optimization

## Configuration
All settings are externalized to environment variables and loaded into `backend/modules/ai/config.py`.
- Defaults to `http://localhost:11434` for Ollama
- Configurable timeouts, context lengths, and retry counts
- Placeholders for future cloud and SAP integrations

## Roadmap
- **Phase 1 (Complete):** Foundation architecture, centralized gateway, Ollama integration.
- **Phase 2 (Complete):** Context Manager expansion, AI Router, Persona Framework, Permission Enforcement.
- **Phase 3:** RAG and embeddings integration, Knowledge Search.
- **Phase 4:** Cloud AI integrations (Gemini, SAP AI).
- **Phase 5:** AI UI components integration.
