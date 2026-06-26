# Backend Startup Guide

**Purpose**: Guide to understanding the backend bootstrap flow and configuration.

## Application Factory (`main.py`)
The backend strictly uses the **Application Factory Pattern** (`create_app()`). This ensures that the application configuration is isolated and instances can be easily tested.

## Lifecycle Management
FastAPI's `@asynccontextmanager` handles the `lifespan` events. 
- **Startup**: Triggers config loading, database connections (future), and logger initialization.
- **Shutdown**: Handles graceful cleanup of connections and tasks.

## Configuration Philosophy (`config/settings.py`)
Configurations are loaded using `pydantic-settings` from environment variables. 
No secrets are hardcoded. We define `Development`, `Testing`, and `Production` placeholders.

## Exception Framework (`exceptions/base.py`)
We use a centralized exception hierarchy derived from `BaseAppException`.
All unhandled exceptions are caught by `middleware/error_handler.py` and converted to standardized JSON responses, preventing stack traces from leaking.

## Logging Philosophy (`logging/logger.py`)
Enterprise standard `logging` is configured at startup. We route discrete streams (App, Error, Audit, Performance).
Currently configured for standard output (Console) with placeholders for file rotating handlers.
