import logging
from neo4j import AsyncGraphDatabase, AsyncDriver
from config.manager import get_config

logger = logging.getLogger("Database.Neo4j")

class Neo4jEngine:
    _driver: AsyncDriver = None

    @classmethod
    async def connect(cls):
        if cls._driver is None:
            config = get_config()
            try:
                cls._driver = AsyncGraphDatabase.driver(
                    config.neo4j.uri, 
                    auth=(config.neo4j.user, config.neo4j.password)
                )
                # Verify connectivity
                await cls._driver.verify_connectivity()
                logger.info("Successfully connected to Neo4j Graph Database.")
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {e}")
                # We do not raise the exception immediately to allow the app to start
                # without Neo4j for dev fallback, but graph operations will fail.
                
    @classmethod
    async def close(cls):
        if cls._driver:
            await cls._driver.close()
            cls._driver = None
            logger.info("Neo4j connection closed.")

    @classmethod
    def get_driver(cls) -> AsyncDriver:
        if cls._driver is None:
            raise RuntimeError("Neo4j driver is not initialized. Call connect() first.")
        return cls._driver
