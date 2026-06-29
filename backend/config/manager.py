from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

from .modules.application import ApplicationSettings, ServerSettings, LoggingSettings
from .modules.database import DatabaseSettings, CachingSettings, RateLimitingSettings, Neo4jSettings
from .modules.security import SecuritySettings, AuthSettings
from .modules.services import EmailSettings, NotificationSettings, StorageSettings
from .modules.integrations import SAPSettings, AISettings
from .modules.business import LearningSettings, AnalyticsSettings

from pydantic import Field

class ConfigManager(BaseSettings):
    app: ApplicationSettings = Field(default_factory=ApplicationSettings)
    server: ServerSettings = Field(default_factory=ServerSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    cache: CachingSettings = Field(default_factory=CachingSettings)
    rate_limit: RateLimitingSettings = Field(default_factory=RateLimitingSettings)
    neo4j: Neo4jSettings = Field(default_factory=Neo4jSettings)
    
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    auth: AuthSettings = Field(default_factory=AuthSettings)
    
    email: EmailSettings = Field(default_factory=EmailSettings)
    notifications: NotificationSettings = Field(default_factory=NotificationSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    
    sap: SAPSettings = Field(default_factory=SAPSettings)
    ai: AISettings = Field(default_factory=AISettings)
    
    learning: LearningSettings = Field(default_factory=LearningSettings)
    analytics: AnalyticsSettings = Field(default_factory=AnalyticsSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache()
def get_config() -> ConfigManager:
    return ConfigManager()
