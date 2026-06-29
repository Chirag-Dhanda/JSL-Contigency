from core.module import BaseModule
from core.di import ServiceContainer
from config.manager import get_config
from .engine import init_engine, close_engine
from logging import getLogger

logger = getLogger("DatabaseModule")

class DatabaseModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Database"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        """Register database-related services (if any)."""
        pass
        
    async def initialize(self) -> None:
        config = get_config()
        if not config.db.database_url:
            logger.warning("DB_DATABASE_URL is not set. Database module may fail.")
        
        init_engine(
            database_url=config.db.database_url,
            pool_size=config.db.pool_size,
            max_overflow=config.db.max_overflow
        )
        
        # Initialize Neo4j
        from .neo4j_engine import Neo4jEngine
        await Neo4jEngine.connect()
        
        logger.info("Database Module Initialized.")
        
    async def shutdown(self) -> None:
        await close_engine()
        from .neo4j_engine import Neo4jEngine
        await Neo4jEngine.close()
        logger.info("Database Module Shutdown.")
