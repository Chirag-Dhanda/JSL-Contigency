"""
Environment & Tenant Management (EP-13).
"""
import logging
from typing import Dict, List, Optional

from .models import TenantEnvironment

logger = logging.getLogger("Administration.EnvironmentManager")


class EnvironmentManager:
    def __init__(self):
        self._environments: Dict[str, TenantEnvironment] = {}
        
        # Seed default environments
        self.register_environment(TenantEnvironment(environment_id="prod", name="Production"))
        self.register_environment(TenantEnvironment(environment_id="stage", name="Staging"))
        self.register_environment(TenantEnvironment(environment_id="dev", name="Development"))

    def register_environment(self, env: TenantEnvironment) -> None:
        self._environments[env.environment_id] = env
        logger.debug(f"Registered environment: {env.name}")

    def get_environment(self, env_id: str) -> Optional[TenantEnvironment]:
        return self._environments.get(env_id)

    def get_all_environments(self) -> List[TenantEnvironment]:
        return list(self._environments.values())
