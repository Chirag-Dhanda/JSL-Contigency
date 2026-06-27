# Enterprise Multi-Agent AI Orchestration Platform

## Overview
Implementation Plan 4.13 transforms the Copilot from a single-agent architecture into a Multi-Agent Orchestrator. Instead of a monolithic AI trying to handle manufacturing specs, safety rules, and HR queries simultaneously, we route complex tasks to isolated, specialized experts and aggregate their answers.

**Strict Limitation**: The Orchestrator is designed strictly for *analytical, read-only* queries (e.g., retrieving knowledge, debugging issues). It does not, and architecturally cannot, execute autonomous physical decisions or production automation commands.

## 1. Orchestrator Engine (`modules/ai_orchestrator`)
The central nervous system.
- **`OrchestratorEngine`**: The main entry point for multi-agent workflows. It follows a strict 3-phase cycle: **Plan** -> **Execute** -> **Aggregate**.
- **`AgentExecutor`**: The runtime loop. It takes the Execution Graph, looks up the agents in the registry, checks if they are online, and runs them sequentially.

## 2. Agent Registry (`modules/agents`)
- **`AgentRegistry`**: A dynamic directory tracking available agents (e.g., `ManufacturingExpert`, `SafetyExpert`).
- **`AgentManifest`**: Defines an agent's capabilities and priority. Crucially, priority dictates conflict resolution (e.g., the Safety Expert has a priority of 100, so its rules override the Manufacturing Expert).

## 3. Task Planning (`modules/task_planning`)
- **`TaskPlanner`**: A semantic router. If a user asks a complex question like "What are the specs and safety rules for the EAF?", the planner detects two distinct intents. It breaks this into an Execution Graph with two steps, assigning Step 1 to `mfg_expert` and Step 2 to `safety_expert`.

## 4. Response Aggregation (`modules/response_aggregation`)
- **`ResponseAggregator`**: Receives the raw outputs from the `AgentExecutor`. It concatenates the answers, deduplicates sources, and prepares a unified JSON payload (`final_answer`, `merged_sources`, `agents_used`) to return to the frontend.

## 5. Frontend Integration
The `OrchestratorDashboard.jsx` provides an administrative view of the multi-agent system.
- **Agent Registry Tab**: Displays all specialized agents, their live health status, capabilities, and conflict priority.
- **Execution Monitoring Tab**: Displays a table of recent multi-agent orchestrations, showing which query invoked which combination of agents, and how many sources were successfully aggregated.
