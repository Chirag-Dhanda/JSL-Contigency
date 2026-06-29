"""
Centralized Health Framework (EP-12).
"""
import logging
import asyncio
from typing import Dict, Callable, Awaitable

from .models import SystemHealth, ComponentHealth, HealthStatus

logger = logging.getLogger("Operations.Health")

# Type for a health check callback function
HealthCheckCallback = Callable[[], Awaitable[ComponentHealth]]


class HealthManager:
    def __init__(self):
        self._checkers: Dict[str, HealthCheckCallback] = {}
        self._last_system_health: SystemHealth = SystemHealth(overall_status=HealthStatus.UNKNOWN)

    def register_component(self, name: str, checker: HealthCheckCallback) -> None:
        """Register a subsystem health check callback."""
        self._checkers[name] = checker
        logger.info(f"Registered health check for component: {name}")

    async def check_all(self) -> SystemHealth:
        """Execute all registered checks and aggregate the results."""
        if not self._checkers:
            return SystemHealth(overall_status=HealthStatus.OK)

        tasks = {name: asyncio.create_task(self._safe_check(name, checker)) 
                 for name, checker in self._checkers.items()}
        
        await asyncio.gather(*tasks.values())
        
        components = {}
        overall_status = HealthStatus.OK
        
        for name, task in tasks.items():
            result = task.result()
            components[name] = result
            
            # Aggregate logic: If any are DOWN, system is DOWN. 
            # If any are DEGRADED, system is DEGRADED unless already DOWN.
            if result.status == HealthStatus.DOWN:
                overall_status = HealthStatus.DOWN
            elif result.status == HealthStatus.DEGRADED and overall_status != HealthStatus.DOWN:
                overall_status = HealthStatus.DEGRADED

        health = SystemHealth(overall_status=overall_status, components=components)
        self._last_system_health = health
        return health

    async def _safe_check(self, name: str, checker: HealthCheckCallback) -> ComponentHealth:
        try:
            # We enforce a timeout so one hung component doesn't block the whole health check
            return await asyncio.wait_for(checker(), timeout=5.0)
        except asyncio.TimeoutError:
            logger.warning(f"Health check timed out for {name}")
            return ComponentHealth(
                component_name=name, 
                status=HealthStatus.DOWN, 
                message="Health check timed out."
            )
        except Exception as e:
            logger.error(f"Health check failed for {name}: {e}")
            return ComponentHealth(
                component_name=name, 
                status=HealthStatus.DOWN, 
                message=str(e)
            )

    def get_last_health(self) -> SystemHealth:
        """Return the most recently calculated health without re-running checks."""
        return self._last_system_health
