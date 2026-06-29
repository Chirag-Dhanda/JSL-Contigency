"""
AI Observability Service (EP-08).
Records per-request metrics for latency, token usage, provider health,
validation outcomes and citation coverage.
Future: replace in-process list with a time-series DB (InfluxDB, Prometheus).
"""
import logging
from typing import Optional, List, Dict, Any
from .models import AIObservabilityRecord

logger = logging.getLogger("AIPlatform.Observability")


class AIObservabilityService:
    def __init__(self):
        self._records: List[AIObservabilityRecord] = []

    def record(
        self,
        skill: str,
        provider: str,
        model: str,
        latency_ms: float,
        total_tokens: int = 0,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        context_passages: int = 0,
        citations_injected: int = 0,
        validation_passed: bool = True,
        conversation_id: Optional[str] = None,
        turn_id: Optional[str] = None
    ) -> None:
        rec = AIObservabilityRecord(
            conversation_id=conversation_id,
            turn_id=turn_id,
            skill=skill,
            provider=provider,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            latency_ms=round(latency_ms, 2),
            context_passages=context_passages,
            citations_injected=citations_injected,
            validation_passed=validation_passed
        )
        self._records.append(rec)
        logger.debug(
            f"[Obs] skill={skill} provider={provider} tokens={total_tokens} "
            f"latency={latency_ms:.1f}ms passages={context_passages} citations={citations_injected} "
            f"valid={validation_passed}"
        )

    def get_summary(self) -> Dict[str, Any]:
        total = len(self._records)
        if total == 0:
            return {"total_requests": 0}

        avg_latency = sum(r.latency_ms for r in self._records) / total
        avg_tokens = sum(r.total_tokens for r in self._records) / total
        validation_failures = sum(1 for r in self._records if not r.validation_passed)

        skill_counts: Dict[str, int] = {}
        provider_counts: Dict[str, int] = {}
        for r in self._records:
            skill_counts[r.skill] = skill_counts.get(r.skill, 0) + 1
            provider_counts[r.provider] = provider_counts.get(r.provider, 0) + 1

        return {
            "total_requests": total,
            "avg_latency_ms": round(avg_latency, 2),
            "avg_tokens_per_request": round(avg_tokens, 1),
            "validation_failure_count": validation_failures,
            "validation_failure_rate": round(validation_failures / total, 3),
            "skill_usage": skill_counts,
            "provider_usage": provider_counts
        }
