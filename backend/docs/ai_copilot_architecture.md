# Enterprise AI Copilot & Conversational Workspace

## Overview
Implementation Plan 4.6 establishes the permanent AI Copilot frontend. Rather than treating AI as a separate page, the Copilot is integrated globally. It actively sniffs the user's current platform location and passes this context to the AI Router (Stage 4.2), allowing for hyper-contextual interactions.

## 1. Copilot Provider & Context Sniffing
The core of the architecture relies on the `CopilotProvider` (React Context). 
- It actively monitors the application router. If a user navigates to `/equipment/arc-furnace`, the Provider updates the internal context to `{ department: "Melting Shop", page: "Arc Furnace" }`.
- When the user types a query, the Provider automatically attaches this context packet alongside the user's message before shipping it to the `EnterpriseAIGateway`.

## 2. Dynamic UI & Prompt Suggestions
- The `AICopilotPanel` provides a flexible, premium user interface supporting docked, expanded, and fullscreen modes styled via strict CSS modules.
- The `PromptSuggestions` component dynamically changes its action buttons based on the sniffed context. If the user is on a standard dashboard, it suggests "Show my training progress". If the user is viewing an SOP, it suggests "Summarize this SOP" or "Identify safety hazards".

## 3. Conversational Workspace
- The `ConversationWorkspace` and `MessageBubble` components handle the visual interaction. They are architected to support Markdown rendering and Syntax Highlighting for clear, readable outputs. 
- The UI strictly differentiates User vs AI messages and includes reserved action slots for "Copy" and "Regenerate".

## 4. Conversation Data Management
- The backend `ConversationManager` and `ConversationModel` were expanded to officially support state flags like `is_pinned` and `title`.
- Secure endpoints ensure that users can Rename, Delete, and Pin their own conversational histories, providing a seamless "Recent Chats" experience in the Copilot's `SidebarManager`.

## Future Integration Nodes
- **Voice/Speech**: Components are structurally prepared to accept Web Speech API hooks for hands-free factory floor usage.
- **Multi-Agent**: The UI can gracefully render multi-agent responses by simply extending the `MessageBubble` to parse different agent roles (e.g., `role: "safety_agent"`).
