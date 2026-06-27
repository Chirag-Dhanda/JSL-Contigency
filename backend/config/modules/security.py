from .base import AppBaseSettings

class SecuritySettings(AppBaseSettings):
    allowed_hosts: str = "*"
    cors_origins: str = "*"
    
    model_config = {"env_prefix": "SEC_"}

class AuthSettings(AppBaseSettings):
    # Required setting without default. Will fail if not provided.
    jwt_secret: str = "super_secret_placeholder_do_not_use_in_prod"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    model_config = {"env_prefix": "AUTH_"}
