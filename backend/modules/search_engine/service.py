"""
Enterprise Search Service (EP-06).
Orchestrates the Planner, Retrieval, Ranking, and Assembly subsystems.
"""
import logging
from typing import List

from .models import SearchRequest, ContextPackage, SearchSession, SearchRecommendation
from .planner import SearchQueryPlanner
from .retrieval import HybridRetrievalEngine
from .ranking import ConfigurableRankingEngine
from .context_assembler import ContextAssemblyEngine

logger = logging.getLogger("SearchEngine.Service")


class EnterpriseSearchService:
    def __init__(
        self,
        planner: SearchQueryPlanner,
        retrieval_engine: HybridRetrievalEngine,
        ranking_engine: ConfigurableRankingEngine,
        context_assembler: ContextAssemblyEngine
    ):
        self.planner = planner
        self.retrieval_engine = retrieval_engine
        self.ranking_engine = ranking_engine
        self.context_assembler = context_assembler

    async def execute_search(self, request: SearchRequest) -> ContextPackage:
        """
        Executes the full Enterprise Search Lifecycle.
        """
        logger.info(f"Executing search for query: '{request.query}'")
        
        # 1. Plan
        plan = self.planner.create_plan(request)

        # 2. Retrieve (Hybrid)
        raw_results = await self.retrieval_engine.execute(request, plan)
        
        # 3. Filter Permissions (Mock for EP-06: we assume basic access if not blocked by DB view)
        # In full implementation, we intersect user_roles with asset.acl here.
        # Currently simulated via the SQL query in KnowledgeRepository filtering by PUBLISHED.

        # 4. Rank
        ranked_passages = self.ranking_engine.rank(raw_results, plan)

        # 5. Assemble Context
        context_package = self.context_assembler.assemble(
            request=request,
            passages=ranked_passages,
            max_tokens=4000 # Configurable limit for downstream LLM
        )

        return context_package


class SearchSessionService:
    """Manages stateful search sessions and recommendations."""
    def __init__(self):
        self._sessions = {} # In-memory mock for EP-06 (Redis in future)

    def create_session(self, user_id: str) -> SearchSession:
        session = SearchSession(user_id=user_id)
        self._sessions[session.session_id] = session
        return session

    def record_query(self, session_id: str, query: str, context_package_id: str):
        if session_id in self._sessions:
            sess = self._sessions[session_id]
            sess.queries.append(query)
            sess.last_context_package_id = context_package_id
            
    def get_recommendations(self, user_department: str) -> List[SearchRecommendation]:
        """Provides basic heuristic recommendations based on department."""
        return [
            SearchRecommendation(
                query=f"Latest SOPs for {user_department or 'my department'}",
                reason="Department Policy"
            ),
            SearchRecommendation(
                query="Safety Procedures",
                reason="Global Compliance"
            )
        ]
