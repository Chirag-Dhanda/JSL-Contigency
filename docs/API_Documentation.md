# API Documentation

## Authentication (`/api/v1/auth`)

### POST `/api/v1/auth/login`
- **Purpose**: Authenticates a user and returns a JWT.
- **Request Body**: `{"username": "admin", "password": "password"}`
- **Response**: `{"access_token": "jwt...", "token_type": "bearer"}`
- **Error Codes**: `401 Unauthorized` (Invalid credentials), `403 Forbidden` (Force Password Change Required).

### POST `/api/v1/auth/change-password`
- **Purpose**: Changes the password for a user.
- **Request Body**: `{"username": "admin", "current_password": "...", "new_password": "..."}`
- **Response**: `{"message": "Password updated successfully"}`

### POST `/api/v1/auth/logout`
- **Purpose**: Invalidates the current JWT token.
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{"message": "Successfully logged out"}`

## Testing & Diagnostics (`/api/v1/test`)

### GET `/api/v1/test/error/not-found`
- **Purpose**: Triggers a standard 404 Exception handled by the global error handler.

### GET `/api/v1/test/error/unhandled`
- **Purpose**: Triggers a raw Python exception to test the 500 fallback handler.

### GET `/api/v1/test/protected`
- **Purpose**: Verifies that the Authorization header middleware is functioning.
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{"message": "You are authenticated!", "sub": "admin"}`

## AI Gateway (Conceptual - via WebSockets/Internal Router)
- **Method**: Stream
- **Payload**: `{"query": "...", "context": {"department": "IT"}}`
- **Permissions**: Requires valid JWT and `ai_query` role permission.
