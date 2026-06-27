# Enterprise Embedding & Synchronization Architecture

## Overview
This architecture orchestrates the continuous translation of raw enterprise knowledge (SOPs, Policies, Equipment Manuals) into highly dimensional vector embeddings using local Ollama models. It ensures that the ChromaDB Vector Store is kept in sync with the primary document repositories automatically.

## Core Modules

### 1. Embeddings Module (`backend/modules/embeddings`)
Provides the central pipeline for translating text to vectors.
- **Provider Layer (`provider.py`)**: Connects to the local Ollama instance (e.g. `nomic-embed-text`) using the centralized AI connection manager. It handles dynamic model discovery, timeouts, and exponential backoff retry logic to handle transient LLM downtime.
- **Engine Layer (`engine.py`)**: Exposes an `asyncio.Queue` based worker system. When requests are submitted, they are placed in a background queue. The worker loop pulls these requests, communicates with the provider, and coordinates with the `VectorDB` to store the output.
- **Metadata Standardization (`models.py`)**: Enforces the `EmbeddingMetadata` schema ensuring that every chunk stored in ChromaDB has a strict identity, including: `document_id`, `chunk_id`, `department`, `security_level`, `version`, and `knowledge_type`.

### 2. Synchronization Engine (`backend/modules/synchronization`)
Acts as the bridge between document creation/updates and the Embedding Engine.
- Exposes semantic operations: `sync_new_document`, `sync_modified_document`, `sync_deleted_document`, and `sync_archived_document`.
- On document modification, the engine safely triggers a partial index rebuild for that specific document before queueing the updated chunks, preventing stale vector data.

### 3. Index Management (`backend/modules/index_management`)
Provides administrative operations for ChromaDB Collections.
- Exposes explicit collection lifecycle controls: `create_index`, `delete_index`, `refresh_index`.
- `partial_rebuild`: Safely purges embeddings for a single document.
- `full_rebuild`: Allows administrators to completely wipe and recreate an index (e.g., when the embedding model is upgraded).

## Background Processing & Health
- **Asynchronous Queues**: The Embedding engine utilizes in-memory Python `asyncio` queues to prevent blocking API requests while documents are being vectorized.
- **Health Monitoring**: The modules export health functions directly to the lifecycle manager. `EmbeddingsModule` verifies Ollama embedding model availability, while `IndexManagementModule` ensures index operations are viable.

## Future Distributed Architecture
Currently, background processing is bound to the ASGI server's memory. As the enterprise knowledge base scales, the `EmbeddingEngine` architecture is designed to be easily swapped with a distributed task queue (like Celery + Redis or RabbitMQ) without modifying the downstream providers or synchronization logic. Dead Letter Queues (DLQ) are stubbed for future implementation to catch and report persistently failing embeddings.
