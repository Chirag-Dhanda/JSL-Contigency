"""
Classification Service (EP-09).
Manages enterprise classification levels and asset tagging.
"""
import logging
from typing import List, Dict

from .models import ClassificationLevel, ClassificationTag

logger = logging.getLogger("Governance.Classification")


class ClassificationService:
    def __init__(self):
        self._asset_tags: Dict[str, ClassificationTag] = {}

    def tag_asset(self, asset_id: str, asset_type: str, level: ClassificationLevel, actor_id: str, reason: str = "") -> ClassificationTag:
        tag = ClassificationTag(
            asset_id=asset_id,
            asset_type=asset_type,
            level=level,
            tagged_by=actor_id,
            reason=reason
        )
        self._asset_tags[asset_id] = tag
        logger.info(f"Asset '{asset_id}' classified as {level.value} by {actor_id}")
        return tag

    def get_asset_classification(self, asset_id: str) -> ClassificationLevel:
        tag = self._asset_tags.get(asset_id)
        if tag:
            return tag.level
        # Default zero-trust fallback if untagged
        return ClassificationLevel.RESTRICTED

    def get_all_tags(self) -> List[ClassificationTag]:
        return list(self._asset_tags.values())
