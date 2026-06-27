# Enterprise Learning Content Management Platform (LCMS)

## Overview
The LCMS (Enterprise Implementation Plan 3.10) provides the robust authoring and cataloging backbone for the entire industrial platform. It strictly enforces version control, sequential managerial approvals, and distinct boundaries between "Work-in-Progress" drafts and "Published" library materials.

## Architectural Separation
The LCMS is split into three distinct modules to separate the authoring lifecycle from public consumption:

### 1. Content Management Module (`content-management`)
This is the restricted "kitchen" where content is authored and reviewed.
- **ContentItem**: Represents a versioned payload. It tracks `VersionInfo` (major/minor bumps, author details, change history).
- **Workflows (`ApprovalWorkflow`)**: Before a draft becomes public, it must be submitted to a workflow. The engine tracks the `active_workflow_state`, moving sequentially (e.g., from `AUTHOR` to `REVIEWER` to `DEPARTMENT_MANAGER`). If rejected, it kicks back to `DRAFT`.
- **Versioning Engine**: The `LCMSEngine` handles creating new versions (e.g., 1.0.0 -> 1.1.0) without destroying the historical record, ensuring compliance and rollback capability.

### 2. Content Library Module (`content-library`)
This is the "storefront". Once an item is fully `APPROVED` and `PUBLISHED`, a wrapper is created here.
- **LibraryItem**: The public-facing catalog item. It is enriched with heavy metadata (`departments`, `equipment_ids`, `tags`) to power the Search Architecture.
- **Collections**: Used to group `LibraryItem`s into Playlists, Role Libraries, or structured Learning Paths.
- **Search Engine**: Exposes a robust search method to filter the library by keyword, role, or specific manufacturing stage.

### 3. Media Module (`media`)
A centralized catalog for raw assets.
- **MediaAsset**: Tracks files like `VIDEO`, `DOCUMENT`, and future `MODEL_3D` or `AR_ASSET`s. This module acts as the Single Source of Truth for storage URLs, allowing one image to be reused across twenty different `ContentItem` SOPs.

## Future AI Integrations
The LCMS models have specifically reserved `ai_metadata_hooks` fields.
When a draft is authored in the future, these hooks will allow background tasks to asynchronously trigger Automatic Summary generation or Semantic Tag Extraction before the content reaches the Reviewer stage.
