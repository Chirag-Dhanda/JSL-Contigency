"""
API Router for Knowledge Platform (EP-05).
"""
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from core.di import container

from modules.auth.middleware import require_authenticated_user
from .models import (
    KnowledgeAsset, IngestionJob, KnowledgeReviewPackage,
    ContextPackage, AssetStatus, KnowledgeAssetSummary
)
from .repository import KnowledgeRepository
from .pipeline.orchestrator import IngestionPipelineOrchestrator
from .review import KnowledgeReviewService

logger = logging.getLogger("KnowledgePlatform.API")
router = APIRouter(prefix="/api/v1/knowledge", tags=["Enterprise Knowledge Platform"])


@router.post("/upload", response_model=IngestionJob)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    asset_type: str = Form("DOCUMENT"),
    department_owner: Optional[str] = Form(None),
    orchestrator: IngestionPipelineOrchestrator = Depends(lambda: container.resolve(IngestionPipelineOrchestrator)),
    repo: KnowledgeRepository = Depends(lambda: container.resolve(KnowledgeRepository)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Uploads a file and kicks off the synchronous ingestion pipeline."""
    file_bytes = await file.read()
    
    asset = KnowledgeAsset(
        title=title,
        asset_type=asset_type,
        department_owner=department_owner,
        created_by=auth_context.get("sub", "system")
    )
    # Save skeleton asset
    asset = await repo.save_asset(asset)
    
    job = IngestionJob(
        asset_id=asset.id,
        filename=file.filename or "unknown",
        file_type=file.content_type or "application/octet-stream",
        submitted_by=auth_context.get("sub", "system")
    )
    job = await repo.save_job(job)

    # In production, this would be `BackgroundTasks.add_task(orchestrator.execute_pipeline, ...)`
    # For EP-05, we await it directly for immediate testability.
    final_job = await orchestrator.execute_pipeline(job.id, file_bytes, job.filename, asset)
    return final_job


@router.get("/jobs/{job_id}", response_model=IngestionJob)
async def get_job_status(
    job_id: str,
    repo: KnowledgeRepository = Depends(lambda: container.resolve(KnowledgeRepository))
):
    return await repo.get_job(job_id)


@router.get("/assets", response_model=List[KnowledgeAssetSummary])
async def list_assets(
    status: Optional[str] = None,
    asset_type: Optional[str] = None,
    repo: KnowledgeRepository = Depends(lambda: container.resolve(KnowledgeRepository))
):
    assets = await repo.list_assets(status=status, asset_type=asset_type)
    return [
        KnowledgeAssetSummary(
            id=a.id, title=a.title, asset_type=a.asset_type,
            status=a.status, version=a.version, department_owner=a.department_owner,
            created_by=a.created_by, created_at=a.created_at
        ) for a in assets
    ]


@router.get("/assets/{asset_id}", response_model=KnowledgeAsset)
async def get_asset(
    asset_id: str,
    repo: KnowledgeRepository = Depends(lambda: container.resolve(KnowledgeRepository))
):
    return await repo.get_asset(asset_id)


@router.post("/assets/{asset_id}/review-package", response_model=KnowledgeReviewPackage)
async def generate_review_package(
    asset_id: str,
    repo: KnowledgeRepository = Depends(lambda: container.resolve(KnowledgeRepository)),
    review_svc: KnowledgeReviewService = Depends(lambda: container.resolve(KnowledgeReviewService))
):
    asset = await repo.get_asset(asset_id)
    return await review_svc.generate_review_package(asset)


@router.post("/assets/{asset_id}/publish", response_model=KnowledgeAsset)
async def publish_asset(
    asset_id: str,
    repo: KnowledgeRepository = Depends(lambda: container.resolve(KnowledgeRepository))
):
    asset = await repo.get_asset(asset_id)
    if asset.status == AssetStatus.PUBLISHED:
        raise HTTPException(status_code=400, detail="Asset is already published.")
        
    asset.status = AssetStatus.PUBLISHED
    
    # In a full graph implementation, this is where we'd push relationships to Neo4j.
    # Graph Projector from EP-04 could be hooked here.
    
    return await repo.save_asset(asset)
