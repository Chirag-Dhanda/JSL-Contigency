import os
from pydantic import BaseModel, Field

class VectorDBConfig(BaseModel):
    # Determine absolute path for persistent storage
    # Assume this file is in backend/modules/vector_db/config.py
    # Project root would be 3 levels up: backend/
    # And then up to the actual project root if backend is a subfolder.
    # The prompt says project_root/storage/chromadb
    
    # We'll use a dynamic path resolution relative to the backend directory or an env var
    backend_root: str = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    project_root: str = os.path.dirname(backend_root)
    
    # Storage settings
    storage_path: str = Field(
        default_factory=lambda: os.getenv("VECTOR_DB_STORAGE_PATH", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", "storage", "chromadb"))
    )
    
    # Operating Mode
    # "persistent" (local chromadb) or "remote" (future cloud/milvus)
    mode: str = os.getenv("VECTOR_DB_MODE", "persistent")
    
    # Remote settings (future)
    remote_host: str = os.getenv("VECTOR_DB_HOST", "localhost")
    remote_port: int = int(os.getenv("VECTOR_DB_PORT", "8000"))
    
    # Collection settings
    default_collections: list[str] = [
        "manufacturing", 
        "safety", 
        "equipment", 
        "sop", 
        "learning", 
        "assessments", 
        "policies", 
        "departments"
    ]
    
    @property
    def collections_path(self) -> str:
        return os.path.join(self.storage_path, "collections")
        
    @property
    def indexes_path(self) -> str:
        return os.path.join(self.storage_path, "indexes")
        
    @property
    def logs_path(self) -> str:
        return os.path.join(self.storage_path, "logs")

vector_db_config = VectorDBConfig()
