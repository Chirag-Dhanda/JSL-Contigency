import logging
from typing import Dict, Any, List
import time

logger = logging.getLogger("RequestQueue")

class RequestQueue:
    """Manages backpressure by buffering incoming AI requests."""
    
    def __init__(self, max_size: int = 20):
        self.max_size = max_size
        self._queue: List[Dict[str, Any]] = []

    def enqueue(self, request_payload: Dict[str, Any]) -> bool:
        """Adds a request to the queue. Returns False if queue is full."""
        if len(self._queue) >= self.max_size:
            logger.warning(f"Backpressure activated: Queue full (max {self.max_size}). Request rejected.")
            return False
            
        # Simplistic queue - in reality this might be priority-based
        request_payload["queued_at"] = time.time()
        self._queue.append(request_payload)
        logger.debug(f"Request enqueued. Queue depth: {len(self._queue)}")
        return True

    def dequeue(self) -> Dict[str, Any]:
        """Pulls the next request from the queue."""
        if self._queue:
            return self._queue.pop(0)
        return None
        
    def get_depth(self) -> int:
        return len(self._queue)
