from fastapi import APIRouter, Depends
from core.di import container
from modules.workspace.models import WorkspaceProfile
from modules.workspace.service import WorkspaceEngineService
from modules.personalization.service import PersonalizationEngineService

router = APIRouter(prefix="/api/workspace", tags=["Experience Platform"])

@router.get("/profile", response_model=WorkspaceProfile)
async def get_workspace_profile(role: str = "ENGINEER", user_id: str = "u-demo"):
    """
    Returns the personalized workspace profile for the authenticated user.
    Mocking the authentication extraction by allowing query parameters.
    """
    workspace_service: WorkspaceEngineService = container.resolve(WorkspaceEngineService)
    personalization_service: PersonalizationEngineService = container.resolve(PersonalizationEngineService)
    
    # 1. Get Base Profile
    profile = workspace_service.get_workspace_for_user(user_id, role)
    
    # 2. AI Personalization
    profile = personalization_service.personalize_workspace(profile)
    
    return profile
