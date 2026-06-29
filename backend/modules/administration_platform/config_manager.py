"""
Enterprise Configuration Platform (EP-13).
"""
import logging
from typing import Dict, List, Any, Optional

from .models import ConfigurationSetting
from .versioning import VersionManager

logger = logging.getLogger("Administration.ConfigManager")


class ConfigManager:
    def __init__(self, version_mgr: VersionManager):
        self._version_mgr = version_mgr
        self._settings: Dict[str, ConfigurationSetting] = {}

    def get_setting(self, key: str) -> Optional[ConfigurationSetting]:
        return self._settings.get(key)

    def get_all_settings(self) -> List[ConfigurationSetting]:
        return list(self._settings.values())

    def set_setting(self, key: str, value: Any, updated_by: str, description: str = "", config_type: str = "string") -> ConfigurationSetting:
        """Updates a configuration and automatically tracks the version change."""
        existing = self._settings.get(key)
        
        setting = ConfigurationSetting(
            key=key,
            value=value,
            type=config_type,
            description=description if description else (existing.description if existing else ""),
            updated_by=updated_by
        )
        
        # Track version change
        old_value = existing.value if existing else None
        if old_value != value:
            self._version_mgr.record_change(
                created_by=updated_by,
                changes={key: {"old": old_value, "new": value}}
            )
            
        self._settings[key] = setting
        logger.info(f"Configuration '{key}' updated by {updated_by}")
        return setting
