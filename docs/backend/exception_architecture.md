# Enterprise Exception Handling & Error Management Framework

**Purpose**: Ensure every crash, validation failure, or business rule violation results in a safe, predictable, and fully observable outcome without leaking sensitive information.

## Exception Hierarchy
We use a structured hierarchy extending `BaseApplicationException`. 
Do NOT raise raw Python `Exception` or `ValueError` in business logic.

### Standard Exceptions
- `ValidationException` (400)
- `AuthenticationException` (401)
- `AuthorizationException` (403)
- `NotFoundException` (404)
- `ConflictException` (409)
- `BusinessRuleException` (400)

### System Exceptions
- `DatabaseException` (500)
- `SAPException` (502)
- `AIException` (502)
- `ConfigurationException` (500)

## Global Exception Handler (`middleware/error_handler.py`)
FastAPI hooks into our handler at the highest level. 
- **Validation**: Pydantic `RequestValidationError` errors are intercepted and translated into our standard API format.
- **Unhandled Exceptions**: If an engineer writes a bug that throws `KeyError`, the handler traps it, logs the full stack trace at the `CRITICAL` level to our logging framework, and returns a sanitized `SYS-500` response to the client.

## Error Codes (`shared/error_codes.py`)
All error responses contain an `error_code` matching a strictly defined registry. Examples:
- `AUTH-401`
- `VAL-400`
- `DB-500`

## Error Response Format
All errors return the `ErrorResponse` JSON model:
```json
{
  "timestamp": "2026-06-26T12:45:00.000Z",
  "status_code": 422,
  "error_code": "REQ-422",
  "title": "Unprocessable Entity",
  "user_message": "The request payload is invalid or malformed.",
  "request_id": "req-12345",
  "path": "/api/v1/auth/login",
  "validation_errors": [
    {
      "loc": ["body", "password"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```
Notice no internal stack traces or internal DB query failures are exposed in the JSON payload.
