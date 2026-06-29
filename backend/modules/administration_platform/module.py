"""
DI Registration for Enterprise Administration Platform (EP-13).
"""
import logging
from typing import Any

from core.module import BaseModule
from core.di import container

from modules.governance_platform.governance_engine import GovernanceEngine

from .versioning import VersionManager
from .config_manager import ConfigManager
from .feature_flags import FeatureManager
from .environment import EnvironmentManager
from .review_center import ReviewCenter

logger = logging.getLogger("AdministrationPlatformModule")


class AdministrationPlatformModule(BaseModule):
    @property
    def name(self) -> str:
        return "AdministrationPlatform"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: Any) -> None:
        logger.info("Registering Enterprise Administration Platform (EP-13) services...")

        version_mgr = VersionManager()
        container.register_singleton(VersionManager, version_mgr)

        config_mgr = ConfigManager(version_mgr)
        container.register_singleton(ConfigManager, config_mgr)

        feature_mgr = FeatureManager(version_mgr)
        container.register_singleton(FeatureManager, feature_mgr)

        env_mgr = EnvironmentManager()
        container.register_singleton(EnvironmentManager, env_mgr)

        gov_engine = container.resolve(GovernanceEngine)
        review_center = ReviewCenter(gov_engine)
        container.register_singleton(ReviewCenter, review_center)

    async def initialize(self) -> None:
        logger.info("Enterprise Administration Platform initialized.")

    async def shutdown(self) -> None:
        pass
