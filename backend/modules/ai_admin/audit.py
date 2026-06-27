import logging
import datetime
from typing import Dict, Any, List

logger = logging.getLogger("AIAuditLogger")

class AIAuditLogger:
    """Strictly logs every AI request for compliance and governance."""
    
    def __init__(self):
        self.logs = [] # Mock DB

    def log_request(self, user_id: str, question: str, model_used: str, success: bool, response_time_ms: int, sources: List[str]) -> bool:
        """Records an interaction."""
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_id": user_id,
            "question": question,
            "model_used": model_used,
            "success": success,
            "response_time_ms": response_time_ms,
            "knowledge_sources_used": sources
        }
        self.logs.append(log_entry)
        logger.info(f"AUDIT LOG: User {user_id} queried model {model_used} | Success: {success}")
        return True
