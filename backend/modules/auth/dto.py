from pydantic import BaseModel
from typing import List

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int

class AuthResponse(TokenResponse):
    pass

class PasswordResetRequest(BaseModel):
    username: str
    current_password: str
    new_password: str

class UserInfoResponse(BaseModel):
    id: str
    username: str
    email: str
    roles: List[str]
    departments: List[str]

class LoginResponse(BaseModel):
    tokens: TokenResponse
    user: UserInfoResponse
