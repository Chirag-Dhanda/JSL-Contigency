from fastapi import APIRouter, Depends
from typing import Dict, Any, List
from pydantic import BaseModel
from core.di import container

from .service import RelationshipEngineService
from .models import EnterpriseRelationship
from modules.relationship_registry.service import RelationshipRegistryService
from modules.relationship_registry.models import RelationshipTypeDefinition
from modules.auth.middleware import require_authenticated_user

router = APIRouter(prefix="/api/v1/relationships", tags=["Enterprise Relationship Engine"])

class CreateRelationshipRequest(BaseModel):
    source_entity_id: str
    target_entity_id: str
    relationship_type: str
    metadata: Dict[str, Any] = {}

# ---------------------------------------------------------
# REGISTRY APIs
# ---------------------------------------------------------

@router.get("/types", response_model=List[RelationshipTypeDefinition])
async def list_relationship_types(
    registry: RelationshipRegistryService = Depends(lambda: container.resolve(RelationshipRegistryService))
):
    return registry.list_types()

@router.post("/types", response_model=RelationshipTypeDefinition)
async def create_relationship_type(
    payload: RelationshipTypeDefinition,
    registry: RelationshipRegistryService = Depends(lambda: container.resolve(RelationshipRegistryService))
):
    return registry.register_type(payload)

# ---------------------------------------------------------
# ENGINE APIs
# ---------------------------------------------------------

@router.post("/", response_model=EnterpriseRelationship)
async def create_relationship(
    payload: CreateRelationshipRequest,
    engine: RelationshipEngineService = Depends(lambda: container.resolve(RelationshipEngineService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    return engine.create_relationship(
        source_id=payload.source_entity_id,
        target_id=payload.target_entity_id,
        rel_type=payload.relationship_type,
        created_by=auth_context.get("sub", "system"),
        metadata=payload.metadata
    )

@router.get("/entity/{entity_id}", response_model=List[EnterpriseRelationship])
async def get_entity_relationships(
    entity_id: str,
    direction: str = "BOTH",
    engine: RelationshipEngineService = Depends(lambda: container.resolve(RelationshipEngineService))
):
    return engine.get_relationships_for_entity(entity_id, direction)
