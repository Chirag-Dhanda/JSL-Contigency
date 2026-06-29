"""
DI Registration for Knowledge Platform (EP-05).
"""
import logging
from typing import Any
from core.di import container
from .repository import KnowledgeRepository
from .parsers.registry import ParserRegistry
from modules.ontology.registry import OntologyRegistryService
from .pipeline.orchestrator import IngestionPipelineOrchestrator
from .quality import KnowledgeQualityService
from .review import KnowledgeReviewService
from modules.relationship_engine.neo4j_repository import Neo4jRepository
from .retrieval import RetrievalPipeline

from core.module import BaseModule

logger = logging.getLogger("KnowledgePlatformModule")


class KnowledgePlatformModule(BaseModule):
    """Initializes and registers all components for the Knowledge Platform."""
    
    @property
    def name(self) -> str:
        return "KnowledgePlatform"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: Any) -> None:
        logger.info("Registering Knowledge Platform (EP-05) services...")

        # Repositories
        repo = KnowledgeRepository()
        container.register_singleton(KnowledgeRepository, repo)

        # Parsers
        parser_registry = ParserRegistry()
        container.register_singleton(ParserRegistry, parser_registry)
        
        # Pipeline
        ontology_registry = container.resolve(OntologyRegistryService)
        orchestrator = IngestionPipelineOrchestrator(repo, parser_registry, ontology_registry)
        container.register_singleton(IngestionPipelineOrchestrator, orchestrator)
        
        # Services
        quality_svc = KnowledgeQualityService(repo)
        container.register_singleton(KnowledgeQualityService, quality_svc)
        
        review_svc = KnowledgeReviewService(repo, quality_svc)
        container.register_singleton(KnowledgeReviewService, review_svc)
        
        # Retrieval
        graph_repo = container.resolve(Neo4jRepository)
        retrieval_pipeline = RetrievalPipeline(repo, graph_repo)
        container.register_singleton(RetrievalPipeline, retrieval_pipeline)

    async def initialize(self) -> None:
        logger.info("Knowledge Platform initialized.")

    async def shutdown(self) -> None:
        pass
