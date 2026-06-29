"""
Platform Version Management (EP-13).
Tracks configuration and operational history for the platform.
"""
import logging
from typing import Dict, List, Any

from .models import ConfigurationVersion

logger = logging.getLogger("Administration.VersionManager")


class VersionManager:
    def __init__(self):
        self._history: List[ConfigurationVersion] = []

    def record_change(self, created_by: str, changes: Dict[str, Any]) -> ConfigurationVersion:
        version = ConfigurationVersion(
            created_by=created_by,
            changes=changes
        )
        self._history.append(version)
        logger.debug(f"Recorded configuration version {version.version_id}")
        return version

    def get_history(self) -> List[ConfigurationVersion]:
        """Returns the history ordered by newest first."""
        return sorted(self._history, key=lambda v: v.timestamp, reverse=True)
