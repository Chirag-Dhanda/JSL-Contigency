from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from core.di import container
from pydantic import BaseModel

from .models import MediaAsset, MediaFilter
from .service import MediaPlatformService
from modules.media_ai.service import MediaAIIntelligenceService
from modules.thumbnail_engine.service import ThumbnailEngineService

router = APIRouter(prefix="/api/media", tags=["Media Platform"])

class UploadAssetRequest(BaseModel):
    filename: str
    file_type: str
    owner: str
    file_size: int

class SearchMediaRequest(BaseModel):
    file_types: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    search_query: Optional[str] = None
    limit: int = 50

@router.post("/upload", response_model=MediaAsset)
async def upload_asset(req: UploadAssetRequest):
    """
    Mocks an upload and synchronously runs the AI processing.
    In reality, file upload would go to S3 and AI processing would be a background task.
    """
    media_service: MediaPlatformService = container.resolve(MediaPlatformService)
    ai_service: MediaAIIntelligenceService = container.resolve(MediaAIIntelligenceService)
    thumbnail_engine: ThumbnailEngineService = container.resolve(ThumbnailEngineService)
    
    # 1. Register Asset
    asset = media_service.register_asset(req.filename, req.file_type, req.owner, req.file_size)
    
    # 2. Run AI Intelligence
    ai_results = ai_service.analyze_asset(asset)
    
    # 3. Update Asset Metadata
    asset = media_service.update_metadata(asset.id, tags=ai_results["suggested_tags"], keywords=ai_results["keywords"])
    
    # 4. Generate Thumbnail (mock)
    _ = thumbnail_engine.generate_thumbnail(asset)
    
    # Note: In a real flow, this would go to a Review Engine before being fully available, 
    # similar to Stage 5.6. For the media API, we assume the upload is direct or pre-approved for simplicity in this stage.
    
    return asset

@router.post("/search", response_model=List[MediaAsset])
async def search_assets(req: SearchMediaRequest):
    media_service: MediaPlatformService = container.resolve(MediaPlatformService)
    
    filter_params = MediaFilter(
        file_types=req.file_types,
        tags=req.tags,
        search_query=req.search_query,
        limit=req.limit
    )
    return media_service.search_assets(filter_params)

@router.get("/{asset_id}", response_model=MediaAsset)
async def get_asset(asset_id: str):
    media_service: MediaPlatformService = container.resolve(MediaPlatformService)
    try:
        return media_service.get_asset(asset_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
