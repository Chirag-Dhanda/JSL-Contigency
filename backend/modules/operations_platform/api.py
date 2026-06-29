"""
Operations Platform API (EP-12).
Provides endpoints for monitoring, health, diagnostics, and backups.
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException

from core.di import container
from modules.auth.middleware import require_authenticated_user

from .models import (
    SystemHealth, MetricRecord, TraceSpan, IncidentRecord, 
    CapacityForecast, BackupRecord
)
from .health import HealthManager
from .telemetry import TelemetryEngine
from .alerts import AlertEngine
from .diagnostics import DiagnosticsEngine
from .backup import BackupManager

router = APIRouter(prefix="/api/v1/operations", tags=["Enterprise Operations"])

# ── Health ───────────────────────────────────────────────────────────────────

@router.get("/health", response_model=SystemHealth)
async def get_system_health(
    force_refresh: bool = False,
    health_mgr: HealthManager = Depends(lambda: container.resolve(HealthManager))
):
    if force_refresh:
        return await health_mgr.check_all()
    return health_mgr.get_last_health()

# ── Telemetry ────────────────────────────────────────────────────────────────

@router.get("/metrics", response_model=List[MetricRecord])
async def get_metrics(
    telemetry: TelemetryEngine = Depends(lambda: container.resolve(TelemetryEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    return telemetry.get_metrics()

@router.get("/traces", response_model=List[TraceSpan])
async def get_traces(
    telemetry: TelemetryEngine = Depends(lambda: container.resolve(TelemetryEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    return telemetry.get_traces()

# ── Alerts & Incidents ───────────────────────────────────────────────────────

@router.get("/incidents", response_model=List[IncidentRecord])
async def get_incidents(
    alerts: AlertEngine = Depends(lambda: container.resolve(AlertEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    return alerts.get_open_incidents()

@router.post("/incidents/{incident_id}/resolve")
async def resolve_incident(
    incident_id: str,
    root_cause: str,
    alerts: AlertEngine = Depends(lambda: container.resolve(AlertEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    try:
        alerts.resolve_incident(incident_id, root_cause)
        return {"message": "Incident resolved."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ── Diagnostics & Capacity ───────────────────────────────────────────────────

@router.get("/diagnostics/slow-queries")
async def get_slow_queries(
    threshold_ms: float = 1000.0,
    diagnostics: DiagnosticsEngine = Depends(lambda: container.resolve(DiagnosticsEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    if "ADMIN" not in auth.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin required.")
    return diagnostics.generate_slow_query_report(threshold_ms)

@router.get("/capacity-forecast", response_model=List[CapacityForecast])
async def get_capacity_forecast(
    diagnostics: DiagnosticsEngine = Depends(lambda: container.resolve(DiagnosticsEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    return diagnostics.forecast_capacity()

# ── Backup & Restore ─────────────────────────────────────────────────────────

@router.get("/backups", response_model=List[BackupRecord])
async def get_backups(
    backup_mgr: BackupManager = Depends(lambda: container.resolve(BackupManager)),
    auth: dict = Depends(require_authenticated_user)
):
    return backup_mgr.get_backups()

@router.post("/backups")
async def trigger_backup(
    component: str,
    backup_mgr: BackupManager = Depends(lambda: container.resolve(BackupManager)),
    auth: dict = Depends(require_authenticated_user)
):
    if "ADMIN" not in auth.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin required.")
    record = backup_mgr.initiate_backup(component)
    return record

@router.post("/backups/{backup_id}/restore")
async def trigger_restore(
    backup_id: str,
    backup_mgr: BackupManager = Depends(lambda: container.resolve(BackupManager)),
    auth: dict = Depends(require_authenticated_user)
):
    if "ADMIN" not in auth.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin required.")
    try:
        pkg_id = backup_mgr.propose_restore(backup_id, auth.get("sub", "system"))
        return {"message": "Restore proposed. Awaiting Governance approval.", "package_id": pkg_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
