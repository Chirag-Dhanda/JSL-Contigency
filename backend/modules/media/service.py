from typing import Dict, List, Optional
from datetime import datetime, timezone
from logging import getLogger
import uuid

from .models import MediaAsset, MediaType

logger = getLogger("MediaEngine")

class MediaEngine:
    def __init__(self):
        self._assets: Dict[str, MediaAsset] = {}

    def upload_asset(self, filename: str, media_type: MediaType, size_bytes: int, mime_type: str, user_id: str) -> MediaAsset:
        """Mocks an upload process for a media asset."""
        asset = MediaAsset(
            id=str(uuid.uuid4()),
            filename=filename,
            media_type=media_type,
            url=f"https://storage.enterprise.local/{media_type.value.lower()}s/{filename}",
            size_bytes=size_bytes,
            mime_type=mime_type,
            uploaded_by_user_id=user_id,
            uploaded_at=datetime.now(timezone.utc)
        )
        self._assets[asset.id] = asset
        logger.info(f"Asset uploaded: {filename} ({asset.id})")
        return asset

    def get_asset(self, asset_id: str) -> Optional[MediaAsset]:
        return self._assets.get(asset_id)

    def search_assets(self, query: str = "", media_type: Optional[MediaType] = None) -> List[MediaAsset]:
        results = []
        for asset in self._assets.values():
            if asset.is_archived:
                continue
            if query and query.lower() not in asset.filename.lower():
                continue
            if media_type and asset.media_type != media_type:
                continue
            results.append(asset)
        return results
