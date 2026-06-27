# Enterprise Embedding Pipeline & Knowledge Synchronization

## Overview
Implementation Plan 4.5 upgrades the basic RAG retrieval structures from Stage 4.3 into a resilient, background-capable, self-healing embedding architecture. It automates the upkeep of the Vector Database by detecting file changes and intelligently updating only the affected records.

## 1. Advanced Embedding Engine & Provider (`modules/embeddings`)
The `EmbeddingEngine` has been completely refactored to rely on the `OllamaEmbeddingProvider`.
- **Dynamic Configuration**: The provider pulls the embedding model (e.g., `nomic-embed-text`) directly from `ai_config` instead of hardcoding strings.
- **Resilience**: Features exponential backoff retries and HTTP timeout handling to ensure the backend survives Ollama API stutters.
- **Background Queue**: An asynchronous `BackgroundQueueManager` prevents massive 100-page document ingestions from blocking the main FastAPI event loop.
- **Extended Metadata**: `EmbeddingMetadata` expands the original `DocumentMetadata` to persistently track exactly which model and version generated a specific vector, paving the way for targeted re-embedding in the future.

## 2. Knowledge Synchronization (`modules/synchronization`)
The `SyncEngine` is the "brain" of index maintenance. 
Rather than blindly rebuilding the entire index every night (which is computationally expensive), the engine computes the delta between the storage buckets and the active vector collections. 
- It detects **New** documents and pushes them to the ingestion pipeline.
- It detects **Deleted** documents and issues pinpoint deletion commands to the vector database.
- It detects **Modified** documents (version bumps) and handles the swap seamlessly.

## 3. Index Management (`modules/index_management`)
The `IndexManager` provides administrative oversight. It exposes capabilities to manually trigger full or partial rebuilds of specific `KnowledgeCollection` (e.g., completely refreshing the `SAFETY` index without touching `MANUFACTURING`).

## 4. Vector DB Health Monitoring (`modules/vector_db/health.py`)
Provides telemetry. It exposes latency, queue depths, and cluster reachability metrics. If latency spikes or the cluster goes offline, the `SyncEngine` can pause operations until health is restored.
