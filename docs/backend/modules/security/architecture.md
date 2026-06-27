# Enterprise Identity Platform Architecture

**Purpose**: Implements the concrete cryptographic foundations for authentication, session revocation, and password security across the JSL platform.

## 1. Security Module (`modules/security/`)
Handles raw cryptographic operations.
- **`JWTService`**: Uses `PyJWT` to encode/decode Access and Refresh tokens. Keys and algorithms (`HS256`) are dynamically loaded from the enterprise `ConfigManager`.
- **`PasswordHasher`**: Uses `passlib[bcrypt]` to enforce industry-standard adaptive hashing. Passwords are never stored in plain text or weakly hashed.

## 2. Sessions Module (`modules/sessions/`)
Maintains the true state of an authenticated user.
- **Why use sessions with stateless JWTs?** JWTs cannot be natively revoked. By embedding a `jti` (JWT ID) into the token and tracking it in `UserSession`, we create a hybrid architecture. The API remains stateless for validation, but the `AuthMiddleware` cross-references the `SessionManager` to ensure the session wasn't explicitly locked or revoked (e.g. by a manager terminating an employee).
- **`LoginHistory`**: An auditable trail of all authentication events, failed attempts, and lockouts, crucial for compliance and brute-force detection.

## 3. Authentication Middleware (`modules/auth/middleware.py`)
The bridge securing the REST API.
- **`require_authenticated_user`**: A FastAPI `Depends` injection that:
  1. Parses the Bearer token from headers.
  2. Cryptographically verifies the signature via `JWTService`.
  3. Checks `SessionManager` to verify the token's `jti` hasn't been revoked.
  4. Yields the verified payload to the router.
- Any failure gracefully raises an `AuthenticationException` formatted as a strict `401 Unauthorized` JSON payload by the global error handler.
