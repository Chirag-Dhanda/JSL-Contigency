# Enterprise Digital SOP Management & Operational Knowledge Architecture

## Overview
The SOP Management Platform (Enterprise Implementation Plan 3.13) provides the core engine for authoring, versioning, and deploying operational procedures. By breaking SOPs down into atomic sections rather than treating them as monolithic documents, the system enables highly targeted rendering and intelligent AI processing.

## Architectural Segregation

### 1. SOP Engine (`sop` module)
The state machine driving the creation and approval of standard operating procedures.
- **SOPDocument**: The root container. It wraps the metadata, workflow state, and a list of `SOPSection` objects. It is assigned an explicit `SOPCategory` (e.g., MANUFACTURING, QUALITY).
- **SOPSection**: The atomic building block of an SOP. Instead of one large text block, an SOP is divided into ordered sections (e.g., Purpose, Scope, Required PPE, Operating Procedure). This granular structure allows the frontend viewer to offer a modular "Reading Progress" experience.
- **SOPMetadata**: Tracks versioning tightly (Revision Number, Version string) alongside effective dates to ensure audit compliance.
- **Approval Workflow**: Managed by the `SOPEngine`, a Draft transitions to `UNDER_REVIEW` and runs through a configurable chain of `WorkflowRole`s (Technical Reviewer -> Manager -> Quality) before achieving `PUBLISHED` status.

### 2. Knowledge Linking (`documentation` module)
To avoid cyclical dependencies between the SOP Engine and previous domains (like Equipment, Safety, and the LCMS), relationships are centralized.
- **LinkedKnowledge**: A mapping object that ties an `sop_id` to arrays of related entities: `equipment_ids`, `manufacturing_stage_ids`, and `safety_module_ids`. When a user reads an SOP, the frontend can cross-reference this model to seamlessly suggest relevant LCMS lessons or Safety protocols.

## Future Integrations
- **AI Processing Hooks**: The `SOPDocument` includes `ai_summary_prompt` and `ai_question_prompt` hooks. Because the SOP is split into `SOPSection`s, future local AI models (like Ollama or Qwen 3.5) can be instructed to summarize specifically the "Operating Procedure" section without being confused by the "Scope" or "References".
- **SAP Synchronization**: `LinkedKnowledge` provisions a `sap_transaction_codes` array, reserving the space necessary to sync digital signatures and document status back to SAP ERP modules in future iterations.
