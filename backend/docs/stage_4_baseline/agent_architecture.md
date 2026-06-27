# Agent Architecture

The Enterprise AI Platform utilizes a Multi-Agent architecture governed by a central Orchestrator.

## The Orchestrator (`OrchestratorEngine`)
The brain of the operation. It does not answer questions directly. Instead, it:
1. Receives the query.
2. Identifies required `capabilities` (e.g., 'specs', 'safety').
3. Looks up registered agents in the `AgentRegistry`.
4. Dispatches sub-tasks to the chosen agents.
5. Aggregates the responses into a cohesive final answer.

## The Agents
Agents are specialized implementations of the `BaseAgent` class. They have narrow domains of expertise.

### 1. Enterprise AI Manufacturing Expert (`mfg_expert`)
- **Domain**: Industrial processes, equipment specifications, telemetry data.
- **Tools**: Has access to live manufacturing databases and technical manuals via RAG.

### 2. Enterprise AI SOP Expert (`safety_expert`)
- **Domain**: Safety, Lockout/Tagout (LOTO), compliance, incident reporting.
- **Constraint**: Must NEVER hallucinate procedures. It relies strictly on approved documentation.

### 3. Enterprise AI Learning Mentor (`learning_mentor`)
- **Domain**: Employee onboarding, skill progression, training recommendations.
- **Tools**: Accesses the employee's `progress` context to suggest the next logical training module.
