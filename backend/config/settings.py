from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Process Contingency JSL - Enterprise API"
    environment: str = "Development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    # Future placeholders
    database_url: str = ""
    jwt_secret: str = ""
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache()
def get_settings():
    return Settings()
