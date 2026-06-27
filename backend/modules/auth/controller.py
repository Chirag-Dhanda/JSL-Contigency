from fastapi import APIRouter, Depends
from core.di import container
from .dto import LoginRequest, AuthResponse, PasswordResetRequest, RefreshTokenRequest, TokenResponse
from .service import AuthService
from .middleware import require_authenticated_user

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_auth_service() -> AuthService:
    return container.resolve(AuthService)

@auth_router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)):
    """Authenticates a user and returns a JWT."""
    return await service.login(payload)

@auth_router.post("/change-password")
async def change_password(payload: PasswordResetRequest, service: AuthService = Depends(get_auth_service)):
    """Processes a First Login forced password change."""
    await service.change_password(payload)
    return {"message": "Password updated successfully. Please log in again."}

@auth_router.post("/logout")
async def logout(payload: dict = Depends(require_authenticated_user), service: AuthService = Depends(get_auth_service)):
    """Revokes the current active session."""
    jti = payload.get("jti")
    if jti:
        await service.logout(jti)
    return {"message": "Logged out successfully."}

@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest, service: AuthService = Depends(get_auth_service)):
    """Refresh an expired JWT access token."""
    return await service.refresh_token(request)
