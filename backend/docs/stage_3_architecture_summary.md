# Stage 3 Architecture Summary: The Digital Factory Twin

## Overview
Stage 3 of the JSL Contingency Learning Platform focused on moving beyond simple users and roles (Stage 1/2) into representing the actual physical and procedural reality of the steel manufacturing enterprise. This collection of modules forms a "Digital Factory Twin"—a strictly typed, interrelated graph of knowledge that a future AI can navigate.

## Core Modules & Their Responsibilities

1. **LCMS (`content_management`, `content_library`, `media`)**
   - *Purpose*: The foundation of traditional learning. Manages version-controlled `LearningModule`s and `MediaAsset`s.

2. **Manufacturing Explorer & Equipment Knowledge (`manufacturing`, `equipment`)**
   - *Purpose*: The spatial and physical mapping. Models the 21-stage steel manufacturing process and ties it to specific `EquipmentNode`s. Crucially, it provisions `scada_tag_id`s, acting as the bridge for future live-IoT integrations.

3. **Safety & Compliance (`safety`, `compliance`, `emergency`)**
   - *Purpose*: The rigorous gatekeepers. The Compliance engine mathematically evaluates a user against regulatory validity periods. The Safety engine structures `Hazard`s to explicit `PPEType`s, while Emergency response maps strict `ContactRole` escalation chains.

4. **SOP Management (`sop`)**
   - *Purpose*: Operational procedure execution. By forcing SOPs into discrete `SOPSection` objects (Purpose, Scope, Procedure), the system allows for targeted AI summarization rather than processing massive text blobs.

5. **Department Hubs & Resource Center (`departments`, `resource_library`)**
   - *Purpose*: The decentralized workspaces. Provides localized landing pages (`DepartmentHub`) while relying on a centralized file index (`ResourceAsset`). The `ResourceRelationship` model is the primary join table holding this massive graph together, linking a single PDF to multiple equipments, safety hazards, and SOPs.

## The Integration Strategy
To prevent cyclic dependencies in Python (`ImportError`), models were designed hierarchically. Broad models (like `LinkedKnowledge` or `ResourceRelationship`) handle the references (via string UUIDs) across the specialized engines, rather than the engines importing each other directly.

The `LearningPlatformOrchestrator` provides the unified facade, initializing these engines and bootstrapping them with JSON-based demo personas and department states.
