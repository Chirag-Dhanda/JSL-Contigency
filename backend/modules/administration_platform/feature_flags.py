"""
Feature Management (EP-13).
"""
import logging
from typing import Dict, List, Optional

from .models import FeatureFlag
from .versioning import VersionManager

logger = logging.getLogger("Administration.FeatureManager")


class FeatureManager:
    def __init__(self, version_mgr: VersionManager):
        self._version_mgr = version_mgr
        self._flags: Dict[str, FeatureFlag] = {}

    def get_flag(self, key: str) -> Optional[FeatureFlag]:
        return self._flags.get(key)

    def get_all_flags(self) -> List[FeatureFlag]:
        return list(self._flags.values())

    def set_flag(self, flag: FeatureFlag, updated_by: str) -> None:
        """Creates or updates a feature flag."""
        existing = self._flags.get(flag.key)
        old_value = existing.is_enabled if existing else None
        
        self._flags[flag.key] = flag
        
        if old_value != flag.is_enabled:
            self._version_mgr.record_change(
                created_by=updated_by,
                changes={f"flag_{flag.key}": {"old": old_value, "new": flag.is_enabled}}
            )
            logger.info(f"Feature flag '{flag.key}' toggled to {flag.is_enabled} by {updated_by}")

    def is_enabled(self, key: str, environment: str = "production", role: Optional[str] = None) -> bool:
        """Evaluates whether a feature is currently enabled for a given context."""
        flag = self._flags.get(key)
        if not flag:
            return False
            
        if not flag.is_enabled:
            return False
            
        if environment not in flag.environments and "*" not in flag.environments:
            return False
            
        if role and role not in flag.allowed_roles and "*" not in flag.allowed_roles:
            return False
            
        return True
