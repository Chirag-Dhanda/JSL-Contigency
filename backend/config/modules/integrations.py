from .base import AppBaseSettings

class SAPSettings(AppBaseSettings):
    sap_host: str = ""
    sap_client: str = ""
    sap_system_number: str = ""
    
    model_config = {"env_prefix": "SAP_"}

class AISettings(AppBaseSettings):
    ollama_url: str = "http://localhost:11434"
    rag_chunk_size: int = 500
    rag_overlap: int = 50
    
    model_config = {"env_prefix": "AI_"}
