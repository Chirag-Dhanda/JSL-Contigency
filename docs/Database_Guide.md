# Database Documentation

The JSL Contingency platform utilizes a dual-database architecture.

## 1. Relational Database (Entities & Relationships)
*Note: In the Stage 4 baseline, these are represented by in-memory mock repositories and Pydantic models. They are designed to map directly to an SQL schema (e.g., PostgreSQL) in Stage 5.*

### Core Tables:
- **`Users`**: `user_id` (PK), `username`, `password_hash`, `requires_password_change`.
- **`Roles`**: `role_id` (PK), `name`.
- **`UserRoles`**: Many-to-Many mapping table.
- **`Permissions`**: `permission_code` (PK), `description`.
- **`RolePermissions`**: Many-to-Many mapping table.

### Operational Tables:
- **`Departments`**: `dept_id` (PK), `name`.
- **`AccessRequests`**: `request_id` (PK), `requester_id` (FK), `target_resource`, `status`, `expires_at`. Tracks Temporary Access.
- **`Events`**: `event_id` (PK), `type`, `payload`, `timestamp`. An event sourcing ledger.
- **`KnowledgeObjects`**: `ko_id` (PK), `title`, `status`, `author_id` (FK). Tracks document metadata.

### Learning Tables:
- **`Roadmaps`**: `roadmap_id` (PK), `title`.
- **`RoadmapNodes`**: `node_id` (PK), `roadmap_id` (FK), `type`.
- **`NodeDependencies`**: Links nodes sequentially.
- **`UserProgress`**: Tracks which nodes a user has unlocked/completed.

## 2. Vector Database (ChromaDB)
Used exclusively for AI Retrieval-Augmented Generation (RAG).

### Collections:
- **`knowledge_base`**: Stores the chunked text and embeddings of all `PUBLISHED` Knowledge Objects.
- **Metadata Indexing**: Each vector chunk stores metadata:
  - `ko_id`: The parent document ID.
  - `department`: For filtering search results (DBAC).
  - `tags`: For rapid semantic filtering.
