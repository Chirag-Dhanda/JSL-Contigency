# Enterprise Notification & Communication Hub

**Purpose**: Establishes a highly decoupled, asynchronous messaging layer that allows any domain module to broadcast events and dispatch rich, localized notifications across various channels (Email, In-App, SMS, Teams) while respecting individual user preferences.

## 1. Enterprise Event Bus (`modules/events/`)
Instead of hardcoding dependencies between domains, modules broadcast `DomainEvent` objects to the `EventBus`.
- **PubSub Model**: The bus uses Python's `asyncio.gather()` to asynchronously execute all registered `EventHandler` callbacks in a fire-and-forget fashion, ensuring the primary thread is never blocked by downstream notification processing.

## 2. Template Engine (`modules/templates/`)
Centralizes all notification content to ensure unified branding and localization.
- Parses templates like `{{ user.name }}` into rendered payloads.
- Defines which delivery channels are supported by specific message types (e.g., A password reset might be Email-only, while a Task Assignment might ping Teams and In-App).

## 3. Multi-Channel Dispatcher (`modules/notifications/`)
The `NotificationService` subscribes to the Event Bus. When triggered:
1. **Renders Template**: Fetches the template and injects dynamic context.
2. **Evaluates Preferences**: Queries the user's `NotificationPreference` to filter out muted channels (or queue for Quiet Hours in the future).
3. **Dispatch**: Routes the `NotificationMessage` through the `DispatcherRegistry` to the exact physical sender (`InAppDispatcher`, `EmailDispatcher`). Currently mocked for functional validation.
