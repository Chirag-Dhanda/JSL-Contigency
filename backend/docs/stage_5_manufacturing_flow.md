# Stage 5.5: Enterprise Manufacturing Flow Builder

This document outlines the architecture for the Manufacturing Flow Builder, introduced in Implementation Plan 5.5.

## 1. Process Modeling (`modules/process_modeling/`)
This module introduces the high-level domain models (`ManufacturingFlow`, `ProcessNode`, `ProcessEdge`) used by the visual editor. 
- A `ProcessNode` represents an entity in the flow (e.g., a Manufacturing Stage, a Quality Gate).
- A `ProcessEdge` represents directional routing logic (e.g., `NEXT_STAGE`, `REWORK`).
- Each node contains a `StageConfiguration` where users define properties like required SOPs, PPE, and estimated duration.

## 2. Process Runtime Engine (`modules/process_runtime/`)
The `ProcessRuntimeEngine` acts as the compiler. When a Master Editor "publishes" a visual flow, the engine:
1. Translates every `ProcessNode` into a concrete `EnterpriseEntity` using the Metadata Engine.
2. Automatically generates `EnterpriseRelationship` edges (via the Relationship Engine) based on the node's configuration (e.g., automatically linking the stage to its mapped Equipment, SOPs, and Department).
3. Connects the generated entities together based on the visual `ProcessEdge` objects to establish the full operational flow in the Knowledge Graph.

## 3. Manufacturing Builder Backend (`modules/manufacturing_builder/`)
Provides the REST API supporting the React frontend. It manages the draft state of flows.
- **AI Assistance**: The `get_ai_suggestions` method scans a draft flow and suggests improvements (e.g., flagging stages that are missing mandatory safety documents or equipment mappings).

## 4. Frontend Visual Flow Editor (`frontend_app/src/modules/manufacturing_builder/`)
Powered by `reactflow`, this module provides a drag-and-drop canvas for process mapping.
- **VisualGraphEditor**: The node canvas.
- **StageConfigurationPanel**: The sidebar where users configure the metadata and review AI suggestions for the selected node.

## 5. Enterprise Demo Seeder
To test the extreme scalability of the platform, a procedural generation script (`demo_seeder.py`) was implemented. It instantly populates the Knowledge Graph with a massive interconnected manufacturing dataset, serving as the foundational context for the upcoming Enterprise AI implementation.
