# Deployment Guide (Stage 4 Baseline)

## Prerequisites
- Python 3.10+
- Node.js 18+
- Ollama (installed locally and running in the background)
- ChromaDB (vector storage)

## 1. Local AI Setup
Ensure Ollama is running and the required models are pulled:
```bash
ollama pull llama3
ollama pull nomic-embed-text
```

## 2. Backend Startup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

## 3. Frontend Startup
```bash
cd frontend_app
npm install
npm run dev
```

## 4. Production Considerations (Future)
For actual production deployment beyond this localized prototype:
- Use Docker Compose to containerize the backend and frontend.
- Deploy ChromaDB as a distributed service.
- Use a dedicated GPU node for Ollama inference.
- Place a reverse proxy (Nginx) in front of the API for SSL termination.
