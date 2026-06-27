# Developer Guide

## 1. Project Setup
Ensure you have Python 3.10+ and Node.js 18+ installed.

### Clone Repository
```bash
git clone <repository_url>
cd jsl_contingency
```

## 2. Backend Startup
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python main.py
```
The backend API runs on `http://localhost:8000`.

## 3. Frontend Startup
```bash
cd frontend_app
npm install
npm run dev
```
The Vite React app runs on `http://localhost:5173`.

## 4. Local AI Services
The platform relies on local AI inference to maintain data privacy.
1. Download and install **Ollama**.
2. Pull the required models:
   ```bash
   ollama pull llama3
   ollama pull nomic-embed-text
   ```
3. Ensure Ollama is running (`http://localhost:11434`).

## 5. Coding Standards
- **Python**: Use `TypeHints` for all function arguments and return types. Use `logging.getLogger(__name__)` instead of `print()`.
- **React**: Use functional components and hooks. Prefer inline styling or CSS modules over global CSS where possible.

## 6. Testing
To run the automated validation test for the AI platform integration:
```bash
cd backend
python verify_stage4.py
```
