import logging
from typing import List, Dict, Optional
from modules.governance.models import VersionRecord
from modules.metadata_engine.service import MetadataEngineService

logger = logging.getLogger("VersionEngine")

class VersionEngineService:
    """
    Maintains immutable snapshots of entities across major/minor/patch lifecycles.
    """
    def __init__(self, meta_engine: MetadataEngineService):
        self.meta_engine = meta_engine
        self._versions: Dict[str, List[VersionRecord]] = {} # entity_id -> [VersionRecord]
        logger.info("Version Engine Initialized.")

    def create_version(self, entity_id: str, author_id: str, bump_type: str = "minor", notes: str = "") -> VersionRecord:
        entity = self.meta_engine.get_entity(entity_id)
        
        history = self._versions.get(entity_id, [])
        
        major, minor, patch = 1, 0, 0
        if history:
            last = history[-1]
            major, minor, patch = last.major_version, last.minor_version, last.patch_version
            if bump_type == "major":
                major += 1; minor = 0; patch = 0
            elif bump_type == "minor":
                minor += 1; patch = 0
            else:
                patch += 1
                
        snapshot = {
            "name": entity.name,
            "display_name": entity.display_name,
            "metadata": dict(entity.metadata) # clone
        }
        
        record = VersionRecord(
            entity_id=entity_id,
            major_version=major,
            minor_version=minor,
            patch_version=patch,
            author_id=author_id,
            snapshot=snapshot,
            version_notes=notes,
            ai_summary=f"Automated AI summary for v{major}.{minor}.{patch}"
        )
        
        if entity_id not in self._versions:
            self._versions[entity_id] = []
        self._versions[entity_id].append(record)
        
        logger.info(f"Versioned {entity_id} to v{major}.{minor}.{patch}")
        return record

    def get_version_history(self, entity_id: str) -> List[VersionRecord]:
        return self._versions.get(entity_id, [])
        
    def rollback(self, entity_id: str, version_id: str) -> bool:
        """Restores a previous snapshot to the active entity."""
        history = self.get_version_history(entity_id)
        target = next((v for v in history if v.id == version_id), None)
        if not target: return False
        
        entity = self.meta_engine.get_entity(entity_id)
        entity.name = target.snapshot["name"]
        entity.display_name = target.snapshot["display_name"]
        entity.metadata = dict(target.snapshot["metadata"])
        logger.warning(f"Rolled back {entity_id} to version {version_id}")
        return True
