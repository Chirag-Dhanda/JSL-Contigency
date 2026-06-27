from pydantic import BaseModel
import os

class AIConfiguration(BaseModel):
    ollama_url: str = os.getenv("AI_OLLAMA_URL", "http://localhost:11434")
    timeout_seconds: int = int(os.getenv("AI_TIMEOUT_SECONDS", "120"))
    max_tokens: int = int(os.getenv("AI_MAX_TOKENS", "4096"))
    temperature: float = float(os.getenv("AI_TEMPERATURE", "0.7"))
    top_p: float = float(os.getenv("AI_TOP_P", "0.9"))
    context_length: int = int(os.getenv("AI_CONTEXT_LENGTH", "8192"))
    streaming_enabled: bool = os.getenv("AI_STREAMING_ENABLED", "True").lower() in ("true", "1")
    retry_count: int = int(os.getenv("AI_RETRY_COUNT", "3"))
    
    # Model configuration
    default_model: str = os.getenv("AI_DEFAULT_MODEL", "qwen2.5:latest")
    embedding_model: str = os.getenv("AI_EMBEDDING_MODEL", "nomic-embed-text:latest")    
    # Future GPU Settings
    gpu_layers: int = int(os.getenv("AI_GPU_LAYERS", "-1")) # -1 for all, 0 for CPU
    cpu_threads: int = int(os.getenv("AI_CPU_THREADS", "4"))
    
    # Future Remote Models
    remote_models_enabled: bool = os.getenv("AI_REMOTE_MODELS_ENABLED", "False").lower() in ("true", "1")
    cloud_ai_api_key: str = os.getenv("AI_CLOUD_API_KEY", "")
    cloud_ai_endpoint: str = os.getenv("AI_CLOUD_ENDPOINT", "")
    sap_ai_endpoint: str = os.getenv("AI_SAP_ENDPOINT", "")

ai_config = AIConfiguration()
