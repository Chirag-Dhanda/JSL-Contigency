"""
Observability Core: Logging, Tracing, Metrics (EP-12).
Prepared for OpenTelemetry exporting in future deployments.
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import contextvars

from .models import TraceSpan, MetricRecord

logger = logging.getLogger("Operations.Telemetry")

# Context variable for distributed tracing correlation
_current_trace_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("trace_id", default=None)
_current_span_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("span_id", default=None)


class TelemetryEngine:
    def __init__(self):
        self._spans: List[TraceSpan] = []
        self._metrics: List[MetricRecord] = []

    # ── Logging ─────────────────────────────────────────────────────────────
    
    def log(self, level: int, message: str, **kwargs) -> None:
        """Structured logging injecting trace IDs if available."""
        trace_id = _current_trace_id.get()
        span_id = _current_span_id.get()
        
        log_payload = {
            "message": message,
            "trace_id": trace_id,
            "span_id": span_id,
            **kwargs
        }
        
        if level == logging.ERROR:
            logger.error(log_payload)
        elif level == logging.WARNING:
            logger.warning(log_payload)
        elif level == logging.INFO:
            logger.info(log_payload)
        else:
            logger.debug(log_payload)

    # ── Tracing ─────────────────────────────────────────────────────────────

    def start_trace(self, trace_id: str) -> None:
        """Initialize a new trace context."""
        _current_trace_id.set(trace_id)

    def start_span(self, operation_name: str, tags: Optional[Dict[str, str]] = None) -> TraceSpan:
        """Start a new span within the current trace."""
        trace_id = _current_trace_id.get()
        if not trace_id:
            import uuid
            trace_id = uuid.uuid4().hex
            self.start_trace(trace_id)
            
        parent_id = _current_span_id.get()
        span = TraceSpan(
            trace_id=trace_id,
            parent_span_id=parent_id,
            operation_name=operation_name,
            start_time=datetime.now(timezone.utc),
            tags=tags or {}
        )
        
        _current_span_id.set(span.span_id)
        self._spans.append(span)
        return span

    def end_span(self, span: TraceSpan) -> None:
        """Close a span."""
        span.end_time = datetime.now(timezone.utc)
        # Restore parent span context
        _current_span_id.set(span.parent_span_id)

    def get_traces(self) -> List[TraceSpan]:
        """Return all collected spans (simulates OTLP exporter)."""
        return self._spans

    # ── Metrics ─────────────────────────────────────────────────────────────

    def record_metric(self, name: str, value: float, unit: str, tags: Optional[Dict[str, str]] = None) -> None:
        """Record a discrete metric."""
        metric = MetricRecord(
            name=name,
            value=value,
            unit=unit,
            tags=tags or {}
        )
        self._metrics.append(metric)

    def get_metrics(self) -> List[MetricRecord]:
        return self._metrics
