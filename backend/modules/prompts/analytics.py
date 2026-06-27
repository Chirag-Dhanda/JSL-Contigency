import logging

logger = logging.getLogger("PromptAnalytics")

class PromptAnalytics:
    """Tracks prompt execution stats (counts, success rates, latency)."""
    
    def __init__(self):
        pass

    def log_execution(self, prompt_id: str, success: bool, latency_ms: int):
        logger.debug(f"Logged execution for prompt {prompt_id}: Success={success}, Latency={latency_ms}ms")
