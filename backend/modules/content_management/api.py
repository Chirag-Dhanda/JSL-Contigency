from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import List, Optional
from core.di import container
from .media import MediaLibraryService
from modules.auth.middleware import require_authenticated_user
from modules.permissions.service import PermissionEngine
from exceptions.base import SystemException

router = APIRouter(prefix="/api/v1/media", tags=["Enterprise Media Library"])

async def require_master_editor(
    auth_context: dict = Depends(require_authenticated_user),
    perm_engine: PermissionEngine = Depends(lambda: container.resolve(PermissionEngine))
):
    """Dependency to enforce MASTER_EDITOR capabilities."""
    user_id = auth_context.get("sub")
    if not await perm_engine.has_explicit_permission(user_id, "media.manage"):
        raise SystemException(message="Insufficient permissions. MASTER_EDITOR required.")
    return auth_context

@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    tags: Optional[str] = Form(None),
    media_service: MediaLibraryService = Depends(lambda: container.resolve(MediaLibraryService)),
    auth_context: dict = Depends(require_master_editor) # Strictly enforced
):
    """Uploads a file to the enterprise storage and registers it in the Metadata Engine."""
    
    # Read file size (mock approach for FastAPI UploadFile)
    await file.seek(0, 2)
    file_size = file.file.tell()
    await file.seek(0)
    
    tag_list = tags.split(",") if tags else []
    
    entity = media_service.upload_asset(
        filename=file.filename,
        content_type=file.content_type,
        file_size=file_size,
        uploaded_by=auth_context.get("sub"),
        tags=tag_list
    )
    
    return {"message": "Upload successful", "entity_id": entity.id, "url": entity.metadata.get("storage_url")}
