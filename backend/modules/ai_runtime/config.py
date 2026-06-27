import logging
from pydantic import BaseModel, Field

logger = logging.getLogger("RuntimeConfig")

class RuntimeConfig(BaseModel):
    """Configuration constraints for the AI Runtime."""
    max_concurrent_requests: int = Field(default=4, description="Maximum number of AI requests processing simultaneously.")
    max_queue_size: int = Field(default=20, description="Maximum number of requests that can be buffered before rejecting.")
    global_timeout_ms: int = Field(default=60000, description="Global timeout for an AI orchestration cycle.")
    cache_ttl_seconds: int = Field(default=3600, description="Time-To-Live for cached responses.")
    retry_limit: int = Field(default=2, description="Maximum automatic retries for a failed task.")
