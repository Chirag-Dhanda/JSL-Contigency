import os
import logging
from typing import Optional

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None

from .config import vector_db_config
from .exceptions import VectorDBConnectionError, VectorDBStorageError

logger = logging.getLogger("VectorDBClient")

class VectorDBClient:
    """Manages the connection to ChromaDB."""
    
    def __init__(self):
        self._client: Optional[chromadb.ClientAPI] = None

    def initialize(self) -> None:
        """Initializes the ChromaDB client, ensuring storage exists."""
        if chromadb is None:
            raise RuntimeError("chromadb package is not installed.")
            
        try:
            self._ensure_storage_directories()
            
            if vector_db_config.mode == "persistent":
                logger.info(f"Initializing Persistent ChromaDB Client at {vector_db_config.storage_path}")
                self._client = chromadb.PersistentClient(
                    path=vector_db_config.storage_path,
                    settings=Settings(
                        anonymized_telemetry=False,
                        allow_reset=False
                    )
                )
            else:
                # Future Remote Integration (e.g., Chroma Server)
                logger.info(f"Initializing Remote ChromaDB Client at {vector_db_config.remote_host}:{vector_db_config.remote_port}")
                self._client = chromadb.HttpClient(
                    host=vector_db_config.remote_host,
                    port=vector_db_config.remote_port
                )
                
            logger.info("ChromaDB Client initialized successfully.")
        except PermissionError as e:
            logger.error(f"Permission denied accessing ChromaDB storage: {e}")
            raise VectorDBStorageError(f"Permission denied accessing storage: {e}") from e
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise VectorDBConnectionError(f"Initialization failed: {e}") from e

    def get_client(self) -> chromadb.ClientAPI:
        """Returns the active ChromaDB client instance."""
        if self._client is None:
            raise VectorDBConnectionError("Client is not initialized. Call initialize() first.")
        return self._client

    def _ensure_storage_directories(self) -> None:
        """Creates the necessary storage directories if they do not exist."""
        try:
            os.makedirs(vector_db_config.storage_path, exist_ok=True)
            os.makedirs(vector_db_config.collections_path, exist_ok=True)
            os.makedirs(vector_db_config.indexes_path, exist_ok=True)
            os.makedirs(vector_db_config.logs_path, exist_ok=True)
        except Exception as e:
            raise VectorDBStorageError(f"Could not create storage directories: {e}") from e

db_client = VectorDBClient()
