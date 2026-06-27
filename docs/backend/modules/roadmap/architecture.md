# Enterprise Learning Roadmap Architecture

**Purpose**: Transforms static onboarding and continuous education into a dynamic, interactive journey using a Directed Acyclic Graph (DAG) state engine.

## 1. Roadmap Node Graph (`modules/roadmap/models.py`)
Learning paths are no longer flat arrays; they are hierarchical structures.
- **Roadmap**: The overarching curriculum (e.g., "JSL Onboarding").
- **RoadmapStage**: Logical groupings (e.g., "Day 1", "Week 1", "Core Safety").
- **RoadmapNode**: The atomic unit of learning (a Video, PDF, Interactive Lesson, or Assessment).
- **RoadmapNodeDependency**: Edges connecting nodes. A node can require multiple mandatory upstream nodes to be completed before it unlocks.

## 2. DAG Execution Engine (`modules/roadmap/engine.py`)
The `RoadmapEngine` is responsible for evaluating the unlock conditions of the graph.
- When `initialize_user_journey()` is called, the engine scans the graph and assigns `UNLOCKED` status to all nodes that have `0` dependencies.
- When a user finishes a lesson, the `mark_node_completed()` service triggers a localized recalculation. The engine iterates over downstream nodes; if a node's `MANDATORY` dependencies evaluate to `COMPLETED`, the engine automatically upgrades the locked node to `UNLOCKED`.

## 3. Frontend Visualization Architecture (`frontend/modules/roadmap/`)
We developed a premium, vanilla UI prototype to prove the user experience:
- **Glassmorphic Canvas**: A sleek, dark-mode canvas utilizing `backdrop-filter: blur()`.
- **SVG Path Connectors**: Native SVG paths (`<path class="connector">`) draw physical lines between nodes. As the DAG Engine unlocks downstream nodes, JavaScript adds an `.active` class to the SVG stroke, illuminating the connection.
- **Progress Ring**: A smooth SVG stroke-dasharray animation accurately renders the user's journey completion percentage.
