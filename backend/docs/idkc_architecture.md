# Industrial Digital Knowledge Center (IDKC) Architecture

## Overview
The Industrial Digital Knowledge Center (IDKC) (Enterprise Implementation Plan 3.11) serves as the definitive digital twin for manufacturing knowledge. It allows users to explore the entire plant via a process flow map, drill down into specific manufacturing stages, and interact with the deep knowledge base of individual equipment units.

## 1. Manufacturing Explorer (`manufacturing` module)
This module dictates the overarching structure of the plant.
- **Manufacturing Stage**: Built upon the `ManufacturingStage` model, representing a distinct step in the lifecycle (e.g., "Electric Arc Furnace"). Each stage tracks its chronological position (`order_index`) and arrays of `equipment_ids` that operate within it.
- **Process Flow**: The `ProcessFlow` model aggregates these stages and defines the relationships using `FlowConnection`s (e.g., tracking that the LRF follows the AOD vessel). This provides the backend structure necessary for the frontend to render interactive Plant Maps.
- **Pre-populated Logic**: The `ManufacturingExplorerService` has been seeded with the 21 standard JSL steel manufacturing stages (from Raw Material Procurement through to Dispatch).

## 2. Equipment Knowledge Center (`equipment` module)
This module acts as the granular encyclopedia for every piece of machinery.
- **Deep Knowledge Structuring**: The `EquipmentKnowledge` model enforces strict tracking of `operating_principle`, `input_materials`, `output_materials`, `troubleshooting_steps`, and `quality_checks`. This standardizes knowledge transfer away from tribal knowledge into a rigid system.
- **Knowledge Relationships**: The `EquipmentRelationship` model acts as a web, linking an equipment unit directly to its relevant SOPs (from LCMS), Lessons (from Knowledge Engine), and Assessments (from Assessment Engine).
- **Engineering Parameters**: The `EngineeringParameter` model prepares for digital twin capabilities. It tracks specific bounds (e.g., Min Temp, Max Temp, Unit) and reserves the `scada_tag_id` and `is_live` flags for future industrial IoT bindings.

## Future Integrations
- **SCADA Bindings**: By mapping `scada_tag_id` on the `EngineeringParameter` model, a future microservice can hydrate this knowledge center with live plant data seamlessly.
- **AI Extensions**: The `AIHooks` model reserves specific prompts (`explain_like_beginner_prompt`, `maintenance_summary_prompt`) allowing an AI Assistant to read the deeply structured Equipment Knowledge and generate dynamic, targeted answers for operators on the floor.
