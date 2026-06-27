# Testing Guide

## 1. Global Integration Testing (`test_startup.py`)
This script tests the entire module lifecycle, dependency injection container, authentication pipelines, and domain routing.
```bash
cd backend
python test_startup.py
```
**Tests Executed:**
- Global Exception Handlers (404, 500).
- DI Container Resolution.
- JWT Authentication (Login, Force Change, Protected Routes).
- Access Governance (Temporary Permissions).
- Event Bus & Notifications.
- Security Headers & Rate Limiting.
- Roadmap DAG Logic.
- Knowledge Status Transitions.

## 2. AI E2E Validation (`verify_stage4.py`)
This script verifies the AI architecture and multi-agent orchestration.
```bash
cd backend
python verify_stage4.py
```
**Tests Executed:**
- **Infrastructure Check**: Verifies Ollama (`localhost:11434`) and ChromaDB are responsive.
- **Permission Check**: Verifies the Gateway blocks restricted users from making queries.
- **RAG Routing**: Verifies the Orchestrator successfully routes manufacturing questions to the `MfgExpert`.
- **Cache Check**: Verifies that identical queries bypass the Orchestrator and return instantly.
