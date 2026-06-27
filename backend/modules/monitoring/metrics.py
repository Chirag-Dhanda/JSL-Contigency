import logging
from typing import List

logger = logging.getLogger("RuntimeMetrics")

class RuntimeMetrics:
    """Tracks granular performance data."""
    
    def __init__(self):
        self.total_requests = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.latencies_ms: List[int] = []

    def record_cache_hit(self, is_hit: bool):
        self.total_requests += 1
        if is_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def record_latency(self, latency_ms: int):
        self.latencies_ms.append(latency_ms)

    def get_metrics_snapshot(self):
        hit_rate = (self.cache_hits / self.total_requests) * 100 if self.total_requests > 0 else 0
        median_latency = sorted(self.latencies_ms)[len(self.latencies_ms)//2] if self.latencies_ms else 0
        
        return {
            "total_requests": self.total_requests,
            "cache_hit_rate_percent": hit_rate,
            "median_latency_ms": median_latency
        }
