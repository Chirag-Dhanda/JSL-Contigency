# ============================================================================

# PART 2

# REPOSITORY STRUCTURE

# ENGINEERING STANDARDS

# ============================================================================

---

# REPOSITORY STRUCTURE

The repository follows a modular enterprise architecture.

Each top-level directory has a single responsibility.

Never place code in an incorrect module simply because it is convenient.

Maintain clear ownership and separation of concerns.

Example structure:

backend/
frontend/
database/
metadata-engine/
relationship-engine/
knowledge-studio/
enterprise-ai-platform/
enterprise-governance-platform/
shared/
sdk/
integrations/
security/
testing/
scripts/
tools/
docs/
demo-data/

Do not introduce new top-level folders unless absolutely necessary.

---

# MODULE OWNERSHIP

Every module must have clear ownership.

A module should expose public interfaces.

Internal implementation details should remain encapsulated.

Avoid cross-module dependencies unless defined through stable interfaces.

Whenever possible:

Module A

↓

Public API

↓

Module B

Never allow direct coupling to internal implementation.

---

# DIRECTORY RULES

Never place backend logic inside frontend folders.

Never place frontend logic inside backend folders.

Never mix documentation with implementation code.

Never place database migration scripts inside application code.

Keep generated assets separate from handwritten code.

Every directory should have a clear purpose.

---

# FILE ORGANIZATION

Prefer multiple small files over one massive file.

Target guidelines:

Python module:
Approximately 200–400 lines.

React component:
Approximately 150–300 lines.

Avoid files exceeding ~800 lines unless there is a compelling architectural reason.

If a file grows excessively, refactor it into smaller modules.

---

# NAMING CONVENTIONS

Use meaningful names.

Examples:

KnowledgeRelationshipService

MetadataRepository

WorkflowExecutionEngine

ManufacturingFlowBuilder

Avoid names like:

Utils

Helper2

Temp

FinalVersion

NewController

ControllerNew

Good names describe business intent.

---

# PYTHON STANDARDS

Use:

snake_case

for:

Functions

Variables

Modules

Use:

PascalCase

for:

Classes

Enums

Dataclasses

Use:

UPPER_CASE

for:

Constants

Configuration Keys

Environment Variables

---

# REACT STANDARDS

React components should use:

PascalCase

Examples:

KnowledgeExplorer.tsx

WorkflowDesigner.tsx

EnterpriseDashboard.tsx

Custom hooks:

useKnowledge()

useWorkflow()

usePermissions()

Avoid anonymous components.

Prefer functional components.

---

# API STANDARDS

REST endpoints should follow consistent naming.

Examples:

/api/v1/knowledge

/api/v1/workflows

/api/v1/media

/api/v1/search

/api/v1/governance

Avoid verbs in URLs where possible.

Use HTTP methods appropriately.

GET

Retrieve

POST

Create

PUT

Replace

PATCH

Partial Update

DELETE

Soft Delete where applicable.

---

# DATABASE STANDARDS

Every database change should be reversible.

Avoid destructive schema changes.

Prefer migrations.

Separate:

Schema

Seed Data

Demo Data

Indexes

Views

Functions

Never mix these responsibilities.

---

# METADATA FIRST

Whenever a new business entity is introduced, ask:

Can this be represented through metadata rather than a new SQL table?

Prefer extending the Metadata Engine over creating new rigid schemas.

Use relational tables only where strong structure and transactional integrity are required.

---

# RELATIONSHIP FIRST

Before adding foreign keys or hardcoded links, ask:

Can this relationship be modeled through the Relationship Engine?

Relationships should remain configurable whenever possible.

Avoid hardcoded business relationships.

---

# REUSABILITY

Before creating a new service or utility:

Search the repository.

If similar functionality already exists:

Reuse it.

Extend it.

Refactor it.

Do not duplicate logic.

---

# ERROR HANDLING

Never silently ignore exceptions.

Provide:

Meaningful error messages.

Structured logging.

Recoverable failures where possible.

Fail safely.

Do not expose sensitive implementation details to users.

---

# LOGGING

Log important events.

Examples:

Authentication

Authorization failures

Workflow execution

Publishing

Version changes

AI requests

Knowledge imports

Use structured logs.

Avoid excessive debug logging in production.

---

# CONFIGURATION

Never hardcode:

Database URLs

API Keys

Secrets

Passwords

Ports

Environment-specific values

Use configuration files and environment variables.

---

# DOCUMENTATION

Every public module should contain documentation covering:

Purpose

Dependencies

Public Interfaces

Security Considerations

Future Expansion

Known Limitations

Update documentation when architecture changes.

---

# TESTING

Design code to be testable.

Favor dependency injection and modular services.

Separate business logic from infrastructure.

Avoid hidden global state.

---

# CODE REVIEW CHECKLIST

Before completing any implementation:

✓ Architecture preserved

✓ Existing modules unaffected

✓ No duplicated logic

✓ Naming conventions followed

✓ Security respected

✓ Documentation updated

✓ Demo data added (where applicable)

✓ Public APIs documented

✓ Errors handled correctly

✓ Future expansion considered

If any item fails, revise the implementation before considering it complete.

---

# ENGINEERING PRINCIPLE

The repository should feel like it is maintained by a professional enterprise software engineering team.

Every change should improve long-term maintainability, consistency and scalability.

Never sacrifice architecture for short-term speed.
