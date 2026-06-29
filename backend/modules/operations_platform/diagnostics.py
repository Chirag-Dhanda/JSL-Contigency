"""
Diagnostics & Capacity Planning (EP-12).
"""
import logging
from typing import List, Dict

from .models import CapacityForecast
from .telemetry import TelemetryEngine

logger = logging.getLogger("Operations.Diagnostics")


class DiagnosticsEngine:
    def __init__(self, telemetry: TelemetryEngine):
        self._telemetry = telemetry

    def generate_slow_query_report(self, threshold_ms: float = 1000.0) -> List[Dict]:
        """Scans traces for spans exceeding a latency threshold."""
        slow_spans = []
        for span in self._telemetry.get_traces():
            duration = span.duration_ms
            if duration and duration > threshold_ms:
                slow_spans.append({
                    "trace_id": span.trace_id,
                    "operation": span.operation_name,
                    "duration_ms": duration,
                    "tags": span.tags
                })
        return slow_spans

    def forecast_capacity(self) -> List[CapacityForecast]:
        """
        Calculates simple linear projections for resource growth based on metrics.
        In a real application, this would query historical DB metrics and run regressions.
        """
        # Mocking forecasts
        return [
            CapacityForecast(
                resource_name="Database Storage",
                current_usage=125.5,
                projected_usage_30d=140.2,
                unit="GB"
            ),
            CapacityForecast(
                resource_name="Vector Index",
                current_usage=10.2,
                projected_usage_30d=15.8,
                unit="GB"
            ),
            CapacityForecast(
                resource_name="AI Tokens",
                current_usage=4500000,
                projected_usage_30d=6000000,
                unit="tokens/month"
            )
        ]
