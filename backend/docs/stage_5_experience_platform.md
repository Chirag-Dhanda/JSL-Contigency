# Stage 5.9: Enterprise Experience Platform

This document outlines the architecture for the Enterprise Experience Platform, which dynamically configures a widget-based personalized workspace for every user based on their Role, Preferences, and AI context.

## 1. Workspace Engine (`modules/workspace/`)
The `WorkspaceEngineService` acts as the layout manager for the backend. It maintains a registry of `DashboardLayout` templates tied to specific enterprise roles (e.g., `MASTER_EDITOR`, `ENGINEER`, `DEFAULT`). 
When a user logs in, it generates a `WorkspaceProfile` that dictatess exactly which widgets they are authorized to see, and how those widgets should be arranged on a grid.

## 2. Personalization Engine (`modules/personalization/`)
The `PersonalizationEngineService` handles user-specific tweaks (themes, accent colors) and simulates the AI Copilot. It inspects the user's role and calculates dynamic recommendations to inject into the `WorkspaceProfile` (e.g., suggesting an Engineer reviews a specific SOP).

## 3. Frontend Experience Platform (`modules/workspace/`)
- **WorkspaceLayout**: The primary entry point. It requests the user's `WorkspaceProfile` from the API and renders a CSS Grid based on the `grid_area` configurations supplied by the backend. It also renders the AI Copilot sidebar.
- **WidgetRegistry**: A core component (`widget_engine/WidgetRegistry.jsx`) that maps abstract widget string IDs (like `system_stats`) directly to functional React components. This allows the backend to completely control the UI layout without hardcoding components on the frontend.
- **Dashboard Studio**: (`modules/dashboard_studio/DashboardStudio.jsx`) A mock administrative interface where a Master Editor or Admin could visually drag and drop widgets to construct the Role Templates that the Workspace Engine uses.

## 4. Scalability
Because the `WidgetRegistry` separates the widget data model from the rendering component, adding new widgets (like a real-time IoT sensor widget or an SAP data table) only requires building the React component and registering it; the Workspace Engine can immediately start assigning it to layouts.
