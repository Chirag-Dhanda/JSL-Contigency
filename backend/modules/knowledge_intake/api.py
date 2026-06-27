from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from typing import List, Dict, Any
from core.di import container
from pydantic import BaseModel

from .models import IntakeJob
from modules.knowledge_architect.orchestrator import KnowledgeArchitectOrchestrator
from modules.review_engine.service import ReviewEngineService

router = APIRouter(prefix="/api/intake", tags=["Knowledge Intake"])

class UploadRequest(BaseModel):
    filename: str
    file_type: str
    uploader: str

@router.post("/upload", response_model=IntakeJob)
async def upload_file(req: UploadRequest):
    """
    Mock endpoint for file upload. In production, this would accept a multipart/form-data.
    """
    architect: KnowledgeArchitectOrchestrator = container.resolve("KnowledgeArchitectOrchestrator")
    job = architect.ingest_file(filename=req.filename, file_type=req.file_type, uploader=req.uploader)
    return job

@router.get("/job/{job_id}", response_model=IntakeJob)
async def get_job_status(job_id: str):
    architect: KnowledgeArchitectOrchestrator = container.resolve("KnowledgeArchitectOrchestrator")
    job = architect.get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/review-queue", response_model=List[IntakeJob])
async def get_review_queue():
    review_engine: ReviewEngineService = container.resolve("ReviewEngineService")
    return review_engine.get_pending_jobs()

@router.post("/review/{job_id}/approve")
async def approve_job(job_id: str, editor_id: str = "master_editor_demo"):
    """
    Approves the job and commits all proposed entities/relationships to the live graph.
    Requires MASTER_EDITOR permissions (mocked here).
    """
    review_engine: ReviewEngineService = container.resolve("ReviewEngineService")
    try:
        review_engine.approve_job(job_id, editor_id)
        return {"status": "approved", "job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/review/{job_id}/reject")
async def reject_job(job_id: str, editor_id: str = "master_editor_demo"):
    review_engine: ReviewEngineService = container.resolve("ReviewEngineService")
    try:
        review_engine.reject_job(job_id, editor_id)
        return {"status": "rejected", "job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
