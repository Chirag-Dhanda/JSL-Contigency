# Logging Architecture & Observability Foundation

**Purpose**: Establish a strict, centralized logging framework ensuring 100% observability across the entire Process Contingency JSL platform.

## Philosophy
- **No Console Printing**: Standard `print()` statements are strictly forbidden. All output must route through the logging framework.
- **Categorization**: Every component must request a dedicated logger (e.g. `logger = logging.getLogger("Database")`) to ensure logs are easily filterable by domain.
- **Context Injection**: Each log entry automatically embeds execution context such as `Request ID`, `User ID`, `Department`, and `Correlation ID`.

## Context Variables (`shared/context.py`)
We leverage Python's native `contextvars` to maintain context without passing state explicitly through every function. 
When a request enters the middleware, a UUID should be generated and set via `set_request_id()`. 

## Log Levels
- `TRACE` (5): Deep granular diagnostics (Custom).
- `DEBUG` (10): Developer debugging flow.
- `INFO` (20): Normal business events.
- `WARNING` (30): Non-fatal anomalies.
- `ERROR` (40): Operation failures.
- `CRITICAL` (50): System panics.

## Standard Log Format
All logs output in the following structure:
```text
[TIMESTAMP] | [LEVEL] | [CATEGORY] | ReqID:[req] | User:[user] | [Message]
```
Example:
```text
2026-06-26 12:45:01 | INFO     | [Application] | ReqID:req-5f8a | User:U-99 | Starting Application in Development mode
```

## Storage & Monitoring Readiness
- Logs stream to `sys.stdout` for container orchestration (Docker/K8s).
- Logs roll automatically into `logs/application.log` and `logs/error.log` (10MB caps).
- Ready for future SIEM, Grafana Promtail, and ELK ingestion by structuring format securely.
