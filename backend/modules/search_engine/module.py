"""
DI Registration for Enterprise Search & Context Engine (EP-06).
"""
import logging
from typing import Any

from core.module import BaseModule
from core.di import container

from .planner import SearchQueryPlanner
from .retrieval import HybridRetrievalEngine
from .ranking import ConfigurableRankingEngine
from .context_assembler import ContextAssemblyEngine
from .service import EnterpriseSearchService, SearchSessionService
from modules.knowledge_platform.repository import KnowledgeRepository
from modules.relationship_engine.neo4j_repository import Neo4jRepository

logger = logging.getLogger("SearchEngineModule")


class SearchEngineModule(BaseModule):
    """Initializes and registers all components for the Enterprise Search & Context Engine."""
    
    @property
    def name(self) -> str:
        return "SearchEngine"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: Any) -> None:
        logger.info("Registering Search Engine (EP-06) services...")

        # Sub-engines
        planner = SearchQueryPlanner()
        container.register_singleton(SearchQueryPlanner, planner)

        pg_repo = container.resolve(KnowledgeRepository)
        graph_repo = container.resolve(Neo4jRepository)
        retrieval = HybridRetrievalEngine(pg_repo, graph_repo)
        container.register_singleton(HybridRetrievalEngine, retrieval)

        ranking = ConfigurableRankingEngine()
        container.register_singleton(ConfigurableRankingEngine, ranking)

        assembler = ContextAssemblyEngine()
        container.register_singleton(ContextAssemblyEngine, assembler)

        # Core Services
        search_svc = EnterpriseSearchService(planner, retrieval, ranking, assembler)
        container.register_singleton(EnterpriseSearchService, search_svc)

        session_svc = SearchSessionService()
        container.register_singleton(SearchSessionService, session_svc)

    async def initialize(self) -> None:
        logger.info("Search Engine initialized.")

    async def shutdown(self) -> None:
        pass
