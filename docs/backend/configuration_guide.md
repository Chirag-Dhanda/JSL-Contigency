# Configuration Guide

**Purpose**: Guide to the Enterprise Configuration Management System.

## Configuration Philosophy
We use a **Centralized Configuration Manager** (`config/manager.py`). 
All configuration values are strictly typed and validated using `pydantic-settings`. 

### Rules:
1. **Never access `os.environ` directly**: Always inject the `ConfigManager` dependency.
2. **Fail Fast**: The application enforces validation at startup (`main.py` -> `validate_config()`). If a required variable like `AUTH_JWT_SECRET` is missing, the backend will refuse to start and print a validation report.

## Environment Structure (`backend/env/`)
Environment templates are stored in `backend/env/`:
- `.env.example`: The default fallback blueprint.
- `development.example`: Development overrides.
- `production.example`: Production profiles (expects secrets to be injected).
- `testing.example`: Testing placeholders.
- `enterprise.example`: High-tier specific JSL configurations (SAP/AD).

To run locally, copy `.env.example` to `.env` in the `backend/` root directory.

## Adding Future Configuration
To add a new setting:
1. Locate the correct domain module in `config/modules/` (e.g. `database.py`, `integrations.py`).
2. Add the typed field to the Pydantic `BaseSettings` class.
3. If it has no default value, it becomes **strictly required** at startup.

## Naming Standards
Every module has an `env_prefix` (e.g. `APP_`, `DB_`, `AUTH_`, `SAP_`). Always follow this standard to avoid collisions.
