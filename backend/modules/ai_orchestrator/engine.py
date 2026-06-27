import logging
from typing import Dict, Any

from modules.agents.registry import AgentRegistry
from modules.task_planning.planner import TaskPlanner
from .executor import AgentExecutor
from modules.response_aggregation.aggregator import ResponseAggregator

logger = logging.getLogger("OrchestratorEngine")

class OrchestratorEngine:
    """The central brain that coordinates planning, execution, and aggregation."""
    
    def __init__(self):
        self.registry = AgentRegistry()
        self.planner = TaskPlanner()
        self.executor = AgentExecutor(self.registry)
        self.aggregator = ResponseAggregator()

    def process_request(self, user_query: str) -> Dict[str, Any]:
        """Main pipeline for a multi-agent request."""
        logger.info(f"ORCHESTRATOR RECEIVED: '{user_query}'")
        
        # 1. Plan
        graph = self.planner.create_execution_graph(user_query)
        
        # 2. Execute
        results = self.executor.execute_graph(graph)
        
        # 3. Aggregate
        final_payload = self.aggregator.aggregate(results)
        
        logger.info("ORCHESTRATION COMPLETE.")
        return final_payload
