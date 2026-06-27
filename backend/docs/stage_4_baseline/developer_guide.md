# Developer Guide

Welcome to the Enterprise AI Platform. This guide outlines how to extend the system without violating the Stage 4 Baseline architecture.

## Golden Rules
1. **Never bypass the Gateway**: All AI requests must go through `EnterpriseAIFacade`. Never instantiate `OllamaClient` directly in UI code.
2. **Never hardcode Prompts**: All prompts must be managed via the `PromptEngine`.
3. **Graceful Degradation**: Always assume the LLM might timeout. Write fallback logic.

## Creating a New Agent
If you need the AI to handle a new domain (e.g., HR Policies):
1. Inherit from `BaseAgent` in `modules/agents/`.
2. Define its `capabilities` (e.g., `["hr", "benefits"]`).
3. Register it with the `AgentRegistry`. The Orchestrator will automatically route relevant questions to it.

## Adding to the Unified Dashboard
If you build a new AI subsystem, ensure you emit telemetry to the `HealthMonitor` so it appears on the `UnifiedHealthDashboard`.
