from .base import AppBaseSettings

class DatabaseSettings(AppBaseSettings):
    database_url: str = "" # Enforce validation later by making this required
    pool_size: int = 5
    max_overflow: int = 10
    
    model_config = {"env_prefix": "DB_"}

class CachingSettings(AppBaseSettings):
    redis_url: str = ""
    
    model_config = {"env_prefix": "CACHE_"}

class RateLimitingSettings(AppBaseSettings):
    rate_limit: int = 100
    
    model_config = {"env_prefix": "RATE_LIMIT_"}

class Neo4jSettings(AppBaseSettings):
    uri: str = "bolt://localhost:7687"
    user: str = "neo4j"
    password: str = "password"
    
    model_config = {"env_prefix": "NEO4J_"}
