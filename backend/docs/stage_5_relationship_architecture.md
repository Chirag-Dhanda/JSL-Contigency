# Stage 5.2: Enterprise Relationship Engine & Knowledge Graph

This document outlines the foundation of Stage 5.2, which introduces a database-independent Knowledge Graph to connect the dynamic entities created in 5.1.

## 1. The Relationship Engine (`modules/relationship_engine/`)
Replaces hardcoded foreign keys and JOIN tables with a generalized `EnterpriseRelationship` model.
- **Connection**: Links `source_entity_id` to `target_entity_id`.
- **Typing**: Uses a registered `relationship_type` (e.g., 'contains', 'depends_on').
- **Metadata**: Just like entities, relationships can hold custom JSON `metadata` on the edge itself (e.g., a 'trained_by' relationship could hold metadata `{"score": 95}`).

## 2. The Relationship Registry (`modules/relationship_registry/`)
The rulebook for connections. It defines what relationships are allowed in the enterprise.
- Registers `RelationshipTypeDefinition`s.
- Enforces directionality (`is_directed`).
- In the future, it can restrict connections via `allowed_source_types` and `allowed_target_types`.

## 3. Knowledge Graph Foundation (`modules/knowledge_graph/`)
An internal graph abstraction that traverses the Entity and Relationship engines without requiring a dedicated graph database like Neo4j.
- `get_neighbours()`: Finds adjacent entities based on edge direction.
- `traverse_bfs()`: Breadth-First Search traversal up to a specified depth.
- `ImpactAnalysisEngine`: Leverages BFS to calculate the "blast radius" of a change. For example, if an SOP is deprecated, it can instantly identify all Equipment and Departments that are impacted.

## 4. Navigation Engine (`modules/navigation_engine/`)
Eliminates hardcoded frontend menus.
- The `DynamicNavigationEngine` builds hierarchical trees on the fly by recursively following specific relationships (e.g., following only 'contains' edges).
- This allows a Department -> Stage -> Equipment tree to automatically expand as new entities are added, with zero code changes.

## 5. Future Extension Strategy
This Knowledge Graph forms the core of the AI Context engine. In future stages, when a user asks "What is the status of the EAF?", the AI Orchestrator can query the Knowledge Graph for the 'EAF' entity, traverse its neighbours, pull its related SOPs and real-time SCADA sensor metadata, and inject the entire sub-graph into the LLM context window.
