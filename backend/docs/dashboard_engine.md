# Enterprise Command Center Dashboard Foundation

## Overview
The Dashboard Engine (Enterprise Implementation Plan 3.8) serves as the central hub for the digital learning platform. Designed to dynamically adapt to a user's role, permissions, and learning progress, the dashboard leverages a robust, polymorphic Widget Framework.

## Widget Framework
The `widgets` module acts as a registry and schema validator for the diverse UI elements that populate a dashboard.
- **Polymorphic Configuration**: Using Pydantic discriminated unions, widgets are strictly defined in `models.py`. A `ProgressWidgetConfig` validates entirely different fields (e.g., `display_style`) compared to a `QuickActionsWidgetConfig` (e.g., list of `QuickActionConfig`).
- **Registry & Permissions**: The `WidgetRegistry` service verifies which widgets a user has permission to load, ensuring that an operator sees safety progress while a manager sees team analytics.

### Supported Widgets
- `WELCOME_CARD`: Personalized greetings.
- `LEARNING_PROGRESS` & `LEARNING_STATISTICS`: High-level data views.
- `CURRENT_ROADMAP` & `TODAYS_TASKS`: Actionable immediate goals.
- `ACTIVITY_FEED`: Stream of recent platform events.
- `QUICK_ACTIONS`: Shortcut buttons for frequent operations.

## Layout System
The `dashboard` module manages how widgets are arranged and personalized on the user's screen.
- **WidgetInstance**: When a widget is assigned to a dashboard, it becomes a `WidgetInstance`. This structure holds the configuration payload alongside standard grid coordinates (`x`, `y`, `w`, `h`), designed to perfectly map to modern frontend responsive grid libraries.
- **DashboardEngine**: This service is responsible for aggregating available widgets and structuring them into a coherent `DashboardLayout`.

## Personalization
The `DashboardPreference` model allows users to tailor their Command Center.
- Supports `ThemeMode` (Light, Dark, System).
- Tracks `favorite_widget_ids` and `hidden_widget_ids`, enabling the frontend to hide or emphasize certain components.

## Activity Feed
The `dashboard` module natively manages a stream of `ActivityItem`s. This supports cross-platform events (e.g., unlocking an achievement in the `achievements` module logs an event here) to ensure the dashboard always feels alive and active.

## Future Integrations
- **AI Widgets**: Custom `AIAssistantWidgetConfig` is prepared to house future conversational elements.
- **SAP Summary**: Prepared `SAPSummaryWidgetConfig` to display external HR or manufacturing metrics seamlessly alongside learning data.
