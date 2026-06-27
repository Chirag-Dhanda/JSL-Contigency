# Enterprise Security Hardening Architecture

**Purpose**: Establishes a perimeter defense for the JSL Application, guaranteeing that malicious payloads and abusive traffic are neutralized before they ever hit the primary business logic controllers.

## 1. Enterprise Security Middleware (`modules/middleware`)
The `EnterpriseSecurityMiddleware` is a Starlette `BaseHTTPMiddleware` mounted globally across the FastAPI instance. It acts as the primary tollbooth for every incoming HTTP request.
- **Interception**: It intercepts requests, executing security protocols, and only calls `call_next(request)` if the validations pass.
- **Ejection**: Throws immediate HTTP Exceptions (handled by our global error handler) if thresholds are violated.

## 2. In-Memory Rate Limiting (`modules/security`)
To protect against brute-force (e.g. against the `/login` endpoint) and general DDoS, the `RateLimiter` enforces a sliding-window bucket algorithm.
- Tracks `client_ip`.
- If a client exceeds the `MAX_REQUESTS` threshold within the `WINDOW_SECONDS`, a `RateLimitExceeded` (Code: 429) exception is thrown.
- **Future Note**: This in-memory implementation serves as the architectural contract for a future Redis-backed implementation.

## 3. Input Sanitization Engine (`modules/validation`)
Before controllers process query strings, the middleware pipes them through the `InputSanitizer`.
- **HTML Stripping**: Aggressively strips `<script>` and `<iframe>` tags using RegEx.
- **XSS Escaping**: Escapes basic `<` and `>` characters to safely display input in dashboards.
- **SQLi Protection**: Strips keywords like `DROP`, `DELETE`, and `UNION` to prevent naive SQL injection attempts.
- **Query Mutability**: The middleware dynamically mutates the ASGI scope's `query_string` so that downstream FastAPI models automatically receive the scrubbed values.

## 4. Immutable Security Headers (`modules/security`)
On the return trip, the middleware intercepts the `Response` object and forcefully injects critical HTTP Security Headers to protect the frontend:
- `Content-Security-Policy`: Restricts where scripts and objects can load from (`default-src 'self'`).
- `X-Frame-Options: DENY`: Prevents Clickjacking by disallowing iframe embedding.
- `Strict-Transport-Security`: Forces HTTPS.
- `X-Content-Type-Options: nosniff`: Prevents MIME-type confusion attacks.
