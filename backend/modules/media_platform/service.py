import logging
from typing import List, Dict, Optional
from datetime import datetime
from .models import MediaAsset, AssetVersion, MediaFilter
from exceptions.base import NotFoundException

logger = logging.getLogger("MediaPlatform")

class MediaPlatformService:
    """
    Core service managing Digital Assets.
    In a real system, this would interact with S3/Blob storage.
    """
    def __init__(self):
        self._assets: Dict[str, MediaAsset] = {}
        logger.info("Media Platform Service Initialized.")

    def register_asset(self, filename: str, file_type: str, owner: str, file_size: int, title: str = None) -> MediaAsset:
        asset = MediaAsset(
            filename=filename,
            file_type=file_type,
            title=title or filename.split('.')[0],
            owner=owner
        )
        
        # Create initial version
        ver = AssetVersion(
            version_number=1,
            file_size_bytes=file_size,
            uploaded_by=owner,
            storage_path=f"mock_storage/{asset.id}/v1/{filename}",
            change_summary="Initial Upload"
        )
        asset.versions.append(ver)
        
        self._assets[asset.id] = asset
        logger.info(f"Registered new media asset: {asset.id} ({filename})")
        return asset

    def get_asset(self, asset_id: str) -> MediaAsset:
        if asset_id not in self._assets:
            raise NotFoundException(message=f"Media Asset {asset_id} not found.")
        return self._assets[asset_id]

    def search_assets(self, filter_params: MediaFilter) -> List[MediaAsset]:
        results = list(self._assets.values())
        
        if filter_params.file_types:
            results = [a for a in results if a.file_type in filter_params.file_types]
            
        if filter_params.tags:
            results = [a for a in results if any(tag in a.tags for tag in filter_params.tags)]
            
        if filter_params.search_query:
            q = filter_params.search_query.lower()
            results = [a for a in results if q in a.title.lower() or q in a.filename.lower() or any(q in k.lower() for k in a.ai_keywords)]
            
        # Sort by updated_at descending
        results.sort(key=lambda x: x.updated_at, reverse=True)
        return results[:filter_params.limit]
        
    def add_new_version(self, asset_id: str, file_size: int, uploader: str, summary: str) -> MediaAsset:
        asset = self.get_asset(asset_id)
        asset.current_version += 1
        
        ver = AssetVersion(
            version_number=asset.current_version,
            file_size_bytes=file_size,
            uploaded_by=uploader,
            storage_path=f"mock_storage/{asset.id}/v{asset.current_version}/{asset.filename}",
            change_summary=summary
        )
        asset.versions.append(ver)
        asset.updated_at = datetime.utcnow()
        
        logger.info(f"Added version {asset.current_version} to {asset.id}")
        return asset
        
    def update_metadata(self, asset_id: str, tags: List[str] = None, keywords: List[str] = None, entity_id: str = None) -> MediaAsset:
        asset = self.get_asset(asset_id)
        if tags is not None:
            asset.tags = tags
        if keywords is not None:
            asset.ai_keywords = keywords
        if entity_id is not None:
            asset.entity_id = entity_id
            
        asset.updated_at = datetime.utcnow()
        return asset
