from .base import AppBaseSettings

class ApplicationSettings(AppBaseSettings):
    app_name: str = "Process Contingency JSL - Enterprise API"
    environment: str = "Development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    
    model_config = {"env_prefix": "APP_"}

class ServerSettings(AppBaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000
    
    model_config = {"env_prefix": "SERVER_"}

class LoggingSettings(AppBaseSettings):
    log_level: str = "INFO"
    
    model_config = {"env_prefix": "LOGGING_"}
