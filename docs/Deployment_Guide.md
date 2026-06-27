# Deployment Guide

This guide details the deployment strategy for the JSL Contingency Platform.

## 1. Required Services
- **FastAPI Backend**: Port 8000
- **React Frontend (Vite)**: Port 5173
- **Ollama**: Port 11434 (Host machine or GPU node)
- **ChromaDB**: Port 8000 (Internal vector storage)

## 2. Environment Variables
Create a `.env` file in the `backend/` directory:
```env
# AI Configuration
OLLAMA_HOST=http://localhost:11434
DEFAULT_LLM_MODEL=llama3
DEFAULT_EMBEDDING_MODEL=nomic-embed-text

# Security
JWT_SECRET=super_secret_enterprise_key_change_in_prod
JWT_EXPIRATION_MINUTES=120

# System Limits
MAX_CONCURRENT_AI_REQUESTS=4
MAX_QUEUE_SIZE=20
```

## 3. Local Deployment (Development)
For local development, refer to the `Developer_Guide.md` to start the backend, frontend, and Ollama services independently.

## 4. Production Deployment (Architecture)
In a production environment, the services should be containerized using Docker.

### Proposed Architecture:
- **API Gateway (Nginx)**: Handles SSL termination and routes traffic.
- **Frontend Container**: Serves the built static React files.
- **Backend Container**: Runs FastAPI via Gunicorn with Uvicorn workers.
- **Vector DB Container**: Runs ChromaDB persistently with volume mounts.
- **GPU Inference Node**: A dedicated bare-metal machine (or GPU-enabled cloud instance) running Ollama to handle the heavy computational load.

### Startup Sequence
1. Start Ollama (Wait for readiness).
2. Start ChromaDB (Wait for readiness).
3. Start FastAPI Backend (The `EnterpriseAIFacade` will initialize and connect to AI services).
4. Start Nginx/Frontend.

## 5. Health Checks
The backend provides a unified health endpoint utilized by the `UnifiedHealthDashboard`.
It aggressively checks the connection to Ollama and ChromaDB. If Ollama fails, the `CircuitBreaker` trips to "Open" state, preventing the backend from hanging on timeouts.

## 6. Backup Strategy
- **Relational Data**: Daily backups of the primary relational database.
- **Vector Data**: The ChromaDB volume mount must be snapshotted daily. Rebuilding the vector index from raw documents is computationally expensive.
