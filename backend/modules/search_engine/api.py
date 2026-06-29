"""
API Router for Enterprise Search & Context Engine (EP-06).
"""
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Form

from core.di import container
from modules.auth.middleware import require_authenticated_user

from .models import SearchRequest, ContextPackage, SearchSession, SearchRecommendation
from .service import EnterpriseSearchService, SearchSessionService

logger = logging.getLogger("SearchEngine.API")
router = APIRouter(prefix="/api/v1/search", tags=["Enterprise Search"])


@router.post("/query", response_model=ContextPackage)
async def execute_search(
    query: str = Form(...),
    asset_types: Optional[List[str]] = Form(None),
    max_results: int = Form(10),
    include_graph_expansion: bool = Form(True),
    search_service: EnterpriseSearchService = Depends(lambda: container.resolve(EnterpriseSearchService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """
    Executes a full context retrieval search. 
    This is the primary endpoint for future LLM or UI integration.
    """
    req = SearchRequest(
        query=query,
        user_department="ENGINEERING", # Mock for EP-06 (extract from auth_context)
        user_roles=["USER"],
        asset_types=asset_types or [],
        max_results=max_results,
        include_graph_expansion=include_graph_expansion
    )
    
    context_pkg = await search_service.execute_search(req)
    return context_pkg


@router.post("/sessions", response_model=SearchSession)
async def create_search_session(
    session_service: SearchSessionService = Depends(lambda: container.resolve(SearchSessionService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    user_id = auth_context.get("sub", "system")
    return session_service.create_session(user_id)


@router.get("/recommendations", response_model=List[SearchRecommendation])
async def get_recommendations(
    department: Optional[str] = Query(None),
    session_service: SearchSessionService = Depends(lambda: container.resolve(SearchSessionService))
):
    return session_service.get_recommendations(user_department=department or "GENERAL")
