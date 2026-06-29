"""
Alerting Engine (EP-12).
Evaluates metrics against rules and generates incidents.
"""
import logging
from typing import Dict, List, Optional

from .models import MetricRecord, AlertRule, AlertSeverity, IncidentRecord

logger = logging.getLogger("Operations.Alerts")


class AlertEngine:
    def __init__(self):
        self._rules: Dict[str, AlertRule] = {}
        self._incidents: Dict[str, IncidentRecord] = {}

    def register_rule(self, rule: AlertRule) -> None:
        self._rules[rule.rule_id] = rule
        logger.info(f"Registered Alert Rule: {rule.metric_name} {rule.condition} {rule.threshold}")

    def evaluate_metric(self, metric: MetricRecord) -> None:
        """Evaluate a new metric against all active rules."""
        for rule in self._rules.values():
            if not rule.is_active or rule.metric_name != metric.name:
                continue

            is_breached = False
            if rule.condition == ">" and metric.value > rule.threshold:
                is_breached = True
            elif rule.condition == "<" and metric.value < rule.threshold:
                is_breached = True
            elif rule.condition == "==" and metric.value == rule.threshold:
                is_breached = True

            if is_breached:
                self._trigger_incident(rule, metric)

    def _trigger_incident(self, rule: AlertRule, metric: MetricRecord) -> None:
        """Create or update an incident based on a rule breach."""
        # Check if an open incident already exists for this rule
        # Simple implementation: one incident per rule to avoid flooding
        open_incidents = [i for i in self._incidents.values() if i.title.startswith(f"Alert Breach: {rule.metric_name}") and i.status != "RESOLVED"]
        
        if open_incidents:
            return  # Suppress duplicate alerts

        incident = IncidentRecord(
            title=f"Alert Breach: {rule.metric_name} {rule.condition} {rule.threshold}",
            severity=rule.severity,
            affected_components=[metric.tags.get("component", "UNKNOWN")]
        )
        self._incidents[incident.incident_id] = incident
        
        logger.warning(f"[INCIDENT CREATED] {incident.title}. Severity: {incident.severity.value}")
        # In a real app, this would publish a DomainEvent to the EventBus to trigger Notifications

    def get_open_incidents(self) -> List[IncidentRecord]:
        return [i for i in self._incidents.values() if i.status != "RESOLVED"]

    def resolve_incident(self, incident_id: str, root_cause: str) -> None:
        from datetime import datetime, timezone
        incident = self._incidents.get(incident_id)
        if incident:
            incident.status = "RESOLVED"
            incident.root_cause = root_cause
            incident.resolved_at = datetime.now(timezone.utc)
            logger.info(f"Incident {incident_id} resolved. Cause: {root_cause}")
