"""
Integration Scheduler (EP-10).
Manages polling and scheduled executions of sync operations.
"""
import logging
import asyncio
from typing import Dict, Any, List, Optional

from .models import SyncSchedule
from .sync_engine import IntegrationSyncEngine

logger = logging.getLogger("Integration.Scheduler")


class IntegrationScheduler:
    def __init__(self, sync_engine: IntegrationSyncEngine):
        self._sync_engine = sync_engine
        self._schedules: Dict[str, SyncSchedule] = {}
        self._task_handles: Dict[str, asyncio.Task] = {}

    def add_schedule(self, schedule: SyncSchedule) -> None:
        self._schedules[schedule.schedule_id] = schedule
        logger.info(f"Added sync schedule {schedule.schedule_id} for connector {schedule.connector_id}")
        
        if schedule.is_active:
            self.start_schedule(schedule.schedule_id)

    def start_schedule(self, schedule_id: str) -> None:
        schedule = self._schedules.get(schedule_id)
        if not schedule:
            raise ValueError(f"Schedule {schedule_id} not found.")
            
        if schedule_id in self._task_handles:
            logger.warning(f"Schedule {schedule_id} is already running.")
            return

        schedule.is_active = True
        
        if schedule.interval_seconds:
            # Create a background polling task
            task = asyncio.create_task(self._poll_loop(schedule))
            self._task_handles[schedule_id] = task
            logger.info(f"Started polling schedule {schedule_id} every {schedule.interval_seconds}s")
        elif schedule.cron_expression:
            logger.info(f"Cron scheduling not fully implemented in mock. ID: {schedule_id}")

    def stop_schedule(self, schedule_id: str) -> None:
        schedule = self._schedules.get(schedule_id)
        if schedule:
            schedule.is_active = False
            
        task = self._task_handles.pop(schedule_id, None)
        if task:
            task.cancel()
            logger.info(f"Stopped schedule {schedule_id}")

    async def _poll_loop(self, schedule: SyncSchedule) -> None:
        while schedule.is_active:
            try:
                # We would normally query all mapped entities, but we'll hardcode 'Equipment' for the mock
                await self._sync_engine.execute_sync(schedule.connector_id, schedule.mode, "Equipment")
                
                from datetime import datetime, timezone
                schedule.last_run = datetime.now(timezone.utc)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in schedule loop {schedule.schedule_id}: {e}")
                
            if schedule.interval_seconds:
                await asyncio.sleep(schedule.interval_seconds)
            else:
                break # safeguard

    def get_schedules(self, connector_id: Optional[str] = None) -> List[SyncSchedule]:
        if connector_id:
            return [s for s in self._schedules.values() if s.connector_id == connector_id]
        return list(self._schedules.values())
