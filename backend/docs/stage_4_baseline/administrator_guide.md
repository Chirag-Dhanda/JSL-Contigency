# Administrator Guide

The AI Administration layer allows non-technical operators to control the AI.

## 1. Unified Health Dashboard
Accessible via the main frontend navigation.
- **Green (Online)**: System is healthy.
- **Red (Offline)**: A critical component is down. If Ollama is offline, the Circuit Breaker will trip, preventing system lockups.

## 2. Performance Monitoring
Use the Performance Dashboard to monitor:
- **Cache Hit Rate**: High cache hit rates mean users are asking FAQ-style questions. This saves compute.
- **Queue Depth**: If Queue Depth frequently hits the maximum (e.g., 20), you need to provision more hardware for the LLM.

## 3. Prompt Studio
To change the AI's behavior, do not ask developers to edit code.
Navigate to the Prompt Studio UI (TBD) and edit the `System Templates`. The AI will instantly adopt the new personality.
