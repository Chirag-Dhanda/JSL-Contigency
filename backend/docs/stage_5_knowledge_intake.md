# Stage 5.6: Enterprise Knowledge Intake Platform

This document outlines the architecture for the AI-driven Enterprise Knowledge Intake Platform.

## 1. Document Understanding (`modules/document_understanding/`)
When a file is uploaded, this module simulates parsing the file's binary contents to extract structured text. It classifies the `document_type` (e.g., SOP, Lesson, Policy) based on the content context.

## 2. Entity Generation (`modules/entity_generation/`)
This module simulates an LLM scanning the extracted text for business entities. It proposes a main entity for the document itself (e.g., creating a new `SOP` entity) and extracts embedded entities (e.g., identifying that a specific `Equipment` is heavily referenced).

## 3. Relationship Discovery & SAP Mapping (`modules/relationship_discovery/`)
This module simulates a graph traversal agent that identifies how the newly proposed entities relate to the rest of the enterprise.
- It proposes logical graph edges (`REFERENCES_EQUIPMENT`, `BELONGS_TO_DEPARTMENT`).
- **SAP Parallel Mapping Strategy**: If SAP-relevant equipment or processes are detected, it creates a `sap_unresolved_mapping` placeholder entity. This guarantees that when a future SAP connector is installed, it can simply fulfill these placeholders rather than requiring a structural database redesign.

## 4. AI Knowledge Architect (`modules/knowledge_architect/`)
The `KnowledgeArchitectOrchestrator` ties the pipeline together. It runs asynchronously in the background, shepherding an `IntakeJob` through the above three services, generating an `ai_summary` of its actions, and finally submitting the complete package to the Review Engine.

## 5. Master Review Center (`modules/review_engine/`)
The system follows a strict "Human in the Loop" policy. AI NEVER publishes automatically. 
- The `ReviewEngineService` holds all AI proposals in an `IN_REVIEW` state.
- The `MASTER_EDITOR` uses the React UI (`ReviewCenter.jsx`) to review the proposed entities and edges.
- Upon approval, the engine maps the proposed IDs to permanent live IDs and commits everything into the `MetadataEngine` and `RelationshipEngine`.

## 6. Frontend Integration
- **Upload Workspace**: (`UploadWorkspace.jsx`) Provides a drag-and-drop interface for users to ingest enterprise documents.
- **Review Center**: (`ReviewCenter.jsx`) Provides the Master Editor with a dashboard detailing the AI's proposed knowledge structures for final approval.
