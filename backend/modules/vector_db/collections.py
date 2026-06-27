import logging
from typing import Dict, List, Any

try:
    import chromadb
except ImportError:
    chromadb = None

from .client import db_client
from .config import vector_db_config
from .exceptions import VectorDBCollectionError

logger = logging.getLogger("CollectionManager")

class CollectionManager:
    """Manages ChromaDB collections registration and lifecycle."""
    
    def __init__(self):
        self._collections: Dict[str, Any] = {}
        
    def register_collections(self) -> None:
        """Ensures all default collections exist in ChromaDB."""
        client = db_client.get_client()
        
        for col_name in vector_db_config.default_collections:
            try:
                # get_or_create_collection is safe and doesn't overwrite existing data
                col = client.get_or_create_collection(
                    name=col_name,
                    metadata={"description": f"Enterprise knowledge base for {col_name}"}
                )
                self._collections[col_name] = col
                logger.debug(f"Registered collection: {col_name}")
            except Exception as e:
                logger.error(f"Failed to register collection '{col_name}': {e}")
                raise VectorDBCollectionError(f"Could not register collection {col_name}: {e}") from e
                
        logger.info(f"Successfully registered {len(self._collections)} default collections.")

    def get_collection(self, name: str) -> Any:
        """Retrieves a registered collection object."""
        if name not in self._collections:
            raise VectorDBCollectionError(f"Collection '{name}' is not registered.")
        return self._collections[name]
        
    def list_collections(self) -> List[str]:
        """Lists all registered collection names."""
        return list(self._collections.keys())

collection_manager = CollectionManager()
