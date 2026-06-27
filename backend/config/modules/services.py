from .base import AppBaseSettings

class EmailSettings(AppBaseSettings):
    smtp_host: str = ""
    smtp_port: int = 587
    
    model_config = {"env_prefix": "EMAIL_"}

class NotificationSettings(AppBaseSettings):
    enable_notifications: bool = False
    
    model_config = {"env_prefix": "NOTIFY_"}

class StorageSettings(AppBaseSettings):
    upload_path: str = "./uploads"
    
    model_config = {"env_prefix": "STORAGE_"}
