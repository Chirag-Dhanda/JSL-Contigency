from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from core.di import container

from .service import MetadataEngineService
from modules.entity_framework.models import EnterpriseEntity
from modules.entity_registry.models import EntityTypeDefinition
from modules.auth.middleware import require_authenticated_user

router = APIRouter(prefix="/api/v1/metadata", tags=["Enterprise Metadata Engine"])

# Request Models
class CreateObjectRequest(BaseModel):
    name: str
    entity_type: str
    display_name: str
    metadata: Dict[str, Any]

class UpdateObjectRequest(BaseModel):
    metadata: Dict[str, Any]

class ValidateObjectRequest(BaseModel):
    type_id: str
    metadata: Dict[str, Any]

# ---------------------------------------------------------
# REGISTRY / TEMPLATE APIs
# ---------------------------------------------------------

@router.get("/types", response_model=List[EntityTypeDefinition])
async def list_metadata_types(
    engine: MetadataEngineService = Depends(lambda: container.resolve(MetadataEngineService))
):
    """List all registered Metadata Types/Templates."""
    return engine.list_types()

@router.post("/types", response_model=EntityTypeDefinition)
async def create_metadata_type(
    payload: EntityTypeDefinition,
    engine: MetadataEngineService = Depends(lambda: container.resolve(MetadataEngineService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Register a new Metadata Type."""
    return engine.register_type(payload)

@router.put("/types/{type_id}", response_model=EntityTypeDefinition)
async def update_metadata_type(
    type_id: str,
    payload: dict,
    engine: MetadataEngineService = Depends(lambda: container.resolve(MetadataEngineService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Update an existing Metadata Type."""
    return engine.update_type(type_id, payload)

@router.delete("/types/{type_id}")
async def delete_metadata_type(
    type_id: str,
    engine: MetadataEngineService = Depends(lambda: container.resolve(MetadataEngineService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Delete a Metadata Type."""
    success = engine.delete_type(type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Type not found")
    return {"message": "Deleted successfully"}

# ---------------------------------------------------------
# OBJECT APIs
# ---------------------------------------------------------

@router.post("/objects", response_model=EnterpriseEntity)
async def create_object(
    payload: CreateObjectRequest,
    engine: MetadataEngineService = Depends(lambda: container.resolve(MetadataEngineService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Create a new dynamic enterprise object."""
    return engine.create_object(
        name=payload.name,
        entity_type=payload.entity_type,
        display_name=payload.display_name,
        created_by=auth_context.get("sub", "system"),
        metadata=payload.metadata
    )

@router.get("/objects/{object_id}", response_model=EnterpriseEntity)
async def get_object(
    object_id: str,
    engine: MetadataEngineService = Depends(lambda: container.resolve(MetadataEngineService))
):
    """Get a specific metadata object."""
    return engine.get_object(object_id)

@router.put("/objects/{object_id}", response_model=EnterpriseEntity)
async def update_object(
    object_id: str,
    payload: UpdateObjectRequest,
    engine: MetadataEngineService = Depends(lambda: container.resolve(MetadataEngineService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Update an existing metadata object."""
    return engine.update_object(
        object_id=object_id,
        new_metadata=payload.metadata,
        user_id=auth_context.get("sub", "system")
    )

@router.get("/search", response_model=List[EnterpriseEntity])
async def search_metadata(
    q: str = Query(..., description="Search query"),
    engine: MetadataEngineService = Depends(lambda: container.resolve(MetadataEngineService))
):
    """Search across all dynamic metadata objects."""
    return engine.search_objects(q)

@router.post("/validate")
async def validate_object(
    payload: ValidateObjectRequest,
    engine: MetadataEngineService = Depends(lambda: container.resolve(MetadataEngineService))
):
    """Dry-run validation against a schema."""
    is_valid = engine.validate_object(payload.type_id, payload.metadata)
    return {"valid": is_valid}
