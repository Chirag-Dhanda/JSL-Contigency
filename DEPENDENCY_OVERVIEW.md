# Dependency Overview
- **Backend Relationships**: API Controllers -> Services -> Repositories -> Database/Integrations.
- **Frontend Relationships**: Pages -> UI Components -> Store/State -> API Client.
- **Database Relationships**: Independent entity schemas with strict foreign keys tied to RBAC/DBAC.
- **Shared Modules**: Interfaces, DTOs, Enums shared between API and internal services.
- **Integration Boundaries**: Third-party APIs (HRMS, Slack) abstracted behind Adapters.
- **Future AI Interactions**: API Controllers -> AI Service Layer -> Ollama Inference Pipeline / Vector Store.
- **Future SAP Interactions**: API Controllers -> SAP Middleware -> BAPI/RFC Connectors -> ERP.
