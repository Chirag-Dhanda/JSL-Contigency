# Enterprise Prompt Studio & Prompt Lifecycle Management

## Overview
Implementation Plan 4.12 addresses the critical issue of "Prompt Drift." In typical AI applications, prompts are often hardcoded directly into business logic (`engine.py`, `service.py`). The Enterprise Prompt Studio extracts all prompts from the codebase and elevates them into a governed, version-controlled repository.

## 1. Prompt Core (`modules/prompts`)
The backbone of the Prompt Studio.
- **`PromptTemplate`**: A rigid schema for all system prompts. It enforces the separation of the `system_prompt` (the persona/rules) from the `prompt_body` (the exact phrasing). It also explicitly tracks expected `variables` (e.g., `{current_user}`).
- **`PromptVersionManager`**: Handles state transitions. Prompts move through strict lifecycles: `DRAFT` -> `REVIEW` -> `APPROVED` -> `PUBLISHED` -> `ARCHIVED`.
- **`PromptDeployer`**: The deployment orchestration module. Only a `PUBLISHED` prompt can be pushed to the active directory for real-time AI agents to use.
- **`PromptGovernance`**: Ensures that prompts pass through approval checks before they can be transitioned to an approved state.

## 2. Prompt Studio Engine (`modules/prompt_studio`)
- **`PromptStudioEngine`**: The central API that the frontend interacts with. It handles creating drafts and managing library categories (Manufacturing, Safety, SOP, etc.).
- **`VariableInjector`**: A universal parser that safely injects standard enterprise context (like `retrieved_knowledge`) into the prompt body using regex mapping.

## 3. Prompt Testing (`modules/prompt_testing`)
- **`PromptTester`**: A sandbox module. Before an author submits a prompt for review, they can use the Tester to inject mock data into the `{variables}`. This allows them to see exactly what the LLM will see, preventing formatting bugs in production.

## 4. Frontend Integration
The `PromptStudioDashboard.jsx` provides the UI for Prompt Engineers.
- **Library Tab**: Displays all prompts, color-coded by their lifecycle status (e.g., green for `PUBLISHED`, yellow for `DRAFT`).
- **Testing Sandbox Tab**: Visually splits the `System Prompt` from the `Raw Template Body`, allowing engineers to preview the exact variables expected by the template.
