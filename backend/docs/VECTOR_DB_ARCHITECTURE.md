# Enterprise Vector Database Architecture (ChromaDB)

## Overview
The Vector Database module provides the foundational infrastructure for future Retrieval-Augmented Generation (RAG) and semantic search capabilities within the JSL Contingency platform. It utilizes **ChromaDB** as the local, production-ready storage engine.

## Core Components (`backend/modules/vector_db`)

### 1. Vector DB Config (`config.py`)
Handles environment variables and dynamic path resolution.
- **Storage Path**: `project_root/storage/chromadb`
- **Default Collections**: `manufacturing`, `safety`, `equipment`, `sop`, `learning`, `assessments`, `policies`, `departments`.

### 2. Database Client (`client.py`)
Encapsulates the ChromaDB persistent client initialization.
- Ensures all persistent storage directories (`collections/`, `indexes/`, `logs/`) are created securely.
- Manages connection lifecycle.

### 3. Collection Manager (`collections.py`)
Orchestrates the creation and retrieval of knowledge collections.
- Safe registration using `get_or_create_collection`.
- Provides internal cataloging of available schemas.

### 4. Health Service (`health.py`)
Provides detailed diagnostics.
- Connection validation
- Storage read/write verification
- Collection enumeration and validation

### 5. Application Integration (`module.py`)
Hooks into the core FastAPI lifecycle via `BaseModule`.
- Initializes ChromaDB on application startup.
- Registers default enterprise collections automatically.
- Mounts health checks for `/api/health`.

## Storage Strategy
All vector embeddings and associated metadata are strictly persisted locally inside the project to ensure data sovereignty and prevent transient data loss:
```
JSL Contingency/
└── storage/
    └── chromadb/
        ├── collections/
        ├── indexes/
        └── logs/
```

## Future Expansion
The architecture is designed to be plug-and-play. If local ChromaDB becomes a bottleneck, the `VectorDBConfig` can be switched to `remote` mode to connect to a remote ChromaDB server, or the `VectorDBClient` can be extended to support alternative backends (Milvus, Pinecone, Qdrant) without modifying the downstream `CollectionManager` or `HealthService`.
