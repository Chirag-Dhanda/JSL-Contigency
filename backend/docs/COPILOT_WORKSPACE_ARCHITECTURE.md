# Enterprise AI Copilot & Workspace Architecture

## Overview
The Enterprise AI Copilot serves as an ever-present, context-aware digital assistant embedded throughout the JSL Contingency platform. It connects users seamlessly to the centralized AI Gateway while respecting all underlying enterprise permissions and tracking long-term conversation memory.

## Architectural Layers

### 1. Conversation Backend (`backend/modules/conversations`)
- **Memory Management**: Captures every message exchanged between the user and the Copilot, timestamping them and saving them to persistent memory (currently mocked in-memory).
- **Domain Models**:
  - `ConversationModel`: Represents the full chat session.
  - `MessageModel`: Represents an individual user prompt or AI response.
  - `ContextBlock`: The critical metadata snapshot (page, role, department, active SOP) captured at the time of the message.
- **Service Layer**: Exposes methods for session creation, context mutation, and message appending.

### 2. Intelligent Copilot Routing (`backend/modules/ai_router/router.py`)
- **`route_copilot_request`**: A specialized routing path that bypasses traditional one-off query patterns. It intercepts the incoming `ContextBlock` to dynamically assign an expert persona (e.g. `MANUFACTURING_EXPERT` if `current_equipment` is set in the UI) before forwarding the request to the central AI Gateway.
- **Session Injection**: Automatically fetches past conversation history from the `ConversationService` and injects it into the prompt generation pipeline, allowing multi-turn conversations.

### 3. Frontend Orchestration (`frontend/modules/ai-copilot`)
- **`CopilotController`**: Central state machine for the UI, handling visual states (Docked, Expanded, Collapsed, Fullscreen).
- **`ContextDetector`**: Global listener that monitors the user's traversal through the application, updating the `ContextBlock` in real-time.
- **`ActionEngine`**: Generates contextually relevant quick-actions (e.g., "Explain this equipment" when viewing an equipment page) to reduce prompt friction.

### 4. UI Components (`frontend/components/ai`)
- **`CopilotPanel`**: The responsive container shell.
- **`ConversationWorkspace`**: The rich-text chat area supporting markdown, code blocks, and future tables/diagrams.
- **`PromptSuggestions`**: Dynamic contextual chips rendered inside the workspace.

## Future Extensibility
- **Long-Term Memory**: The backend is structured to eventually summarize and compress older conversations to persist across multiple sessions.
- **Streaming & Voice**: Hooks are prepared in the frontend and gateway layers to easily attach WebSockets for live typing and text-to-speech generation.
- **Live Data Connectors**: The `ContextBlock` can be expanded to include live telemetry from SCADA or SAP systems, injecting realtime statistics seamlessly into the AI's awareness.
