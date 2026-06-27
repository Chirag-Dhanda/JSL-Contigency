# Stage 5.3: Enterprise Knowledge Studio

This document outlines the foundation of Stage 5.3, which introduces a dedicated workspace for authorized users to visually manage the Enterprise Knowledge Graph.

## 1. Role: `MASTER_EDITOR`
A new authorization role has been introduced. Unlike system administrators, the `MASTER_EDITOR` cannot modify authentication, user records, or platform configuration. Their permissions are strictly scoped to the Knowledge Graph:
- `entity.create`, `entity.modify`, `entity.archive`, `entity.restore`, `entity.version.manage`
- `relationship.create`, `relationship.modify`
- `media.manage`, `knowledge.manage`
- `content.publish`, `content.draft.view`
- `ai.suggestions.review`

## 2. Knowledge Studio React Dashboard
The frontend now includes a dedicated React layout (`KnowledgeStudioLayout.jsx`) operating completely independently from the standard user dashboards. It provides shells for:
- **Entity Explorer**: For managing dynamic entities.
- **Relationship Explorer**: For managing graph edges.
- **Media Library**: For uploading and tagging physical assets (PDFs, images).
- **Publishing Center**: For managing content states.
- **AI Review Queue**: For accepting/rejecting orchestrator suggestions.

## 3. Media & Content Management (`modules/content_management/`)
Assets (like PDFs and images) are no longer treated as isolated files. They are uploaded, stored (mocked as an external S3 URL), and instantly registered in the Metadata Engine as an `EnterpriseEntity` of type `media_asset`. This allows media to be fully integrated into the Knowledge Graph (e.g., an SOP entity can have a `references` relationship pointing directly to a Media Asset entity).

## 4. Publishing Engine (`modules/publishing/`)
The `PublishingWorkflowService` enforces a strict state machine on all entities.
- Draft -> Review -> Approved -> Published.
- Ensures that standard users cannot see unfinished entities or relationships in the AI Copilot.

## 5. AI Review Queue (`modules/knowledge_studio/ai_review.py`)
Because the Enterprise AI Orchestrator acts autonomously, it will generate summaries, extract tags, or suggest relationship links. The AI Review Queue intercepts these suggestions and holds them in a `PENDING` state until a human `MASTER_EDITOR` explicitly approves or rejects them.
