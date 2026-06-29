"""
Query Planner for Enterprise Search (EP-06).
Determines search strategies before hitting the database.
"""
import logging
from typing import List
from .models import SearchRequest, RetrievalPlan, RetrievalStrategy

logger = logging.getLogger("SearchEngine.Planner")


class SearchQueryPlanner:
    """
    Optimizes queries and determines required search axes.
    """

    def create_plan(self, request: SearchRequest) -> RetrievalPlan:
        # 1. Clean query
        optimized_query = request.query.strip().lower()

        # 2. Determine Strategy Weights
        strategies: List[RetrievalStrategy] = []
        
        # Lexical is always base
        strategies.append(RetrievalStrategy(name="lexical", weight=0.3))
        
        # Vector search if query is > 2 words
        if len(optimized_query.split()) > 2:
            strategies.append(RetrievalStrategy(name="vector", weight=0.5))
        else:
            strategies.append(RetrievalStrategy(name="vector", weight=0.2))

        # Graph expansion if requested
        if request.include_graph_expansion:
            strategies.append(RetrievalStrategy(name="graph", weight=0.1))

        # Ontology mapping
        strategies.append(RetrievalStrategy(name="ontology", weight=0.1))

        # 3. Determine Required Departments / Filters
        target_depts = []
        if request.user_department:
            target_depts.append(request.user_department)

        plan = RetrievalPlan(
            original_query=request.query,
            optimized_query=optimized_query,
            strategies=strategies,
            target_asset_types=request.asset_types,
            required_departments=target_depts
        )
        
        logger.info(f"[{plan.plan_id}] Generated retrieval plan for query: '{request.query}'")
        return plan
