import logging
from typing import Dict, Any

from .config import ai_config
from .connection import connection_manager

logger = logging.getLogger("AIHealthChecker")

class AIHealthChecker:
    """Manages the health checks to the local Ollama instance."""
    
    @staticmethod
    async def check_health() -> bool:
        try:
            response = await connection_manager.request_with_retry("GET", "/api/version")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama Health Check Failed: {e}")
            return False
            
    @staticmethod
    async def get_health_details() -> Dict[str, Any]:
        """Get detailed health status."""
        is_healthy = await AIHealthChecker.check_health()
        return {
            "status": "up" if is_healthy else "down",
            "url": ai_config.ollama_url,
            "retry_count": ai_config.retry_count,
            "timeout": ai_config.timeout_seconds
        }
