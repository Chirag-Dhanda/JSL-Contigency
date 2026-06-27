import logging
from typing import Dict, List, Any
from modules.agents.registry import AgentRegistry

logger = logging.getLogger("AgentExecutor")

class AgentExecutor:
    """Handles the sequential execution of the task graph."""
    
    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    def execute_graph(self, graph: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Runs the tasks against the mock agents."""
        logger.info(f"Executing graph with {len(graph)} steps.")
        results = []
        
        for node in graph:
            agent_id = node["agent_id"]
            agent = self.registry.get_agent(agent_id)
            
            if not agent or agent.status != "Online":
                logger.warning(f"Agent {agent_id} is unavailable. Skipping step.")
                continue
                
            logger.debug(f"Invoking {agent.name} for task: {node['task']}")
            
            # Mock Agent Execution
            mock_output = ""
            mock_sources = []
            
            if agent_id == "mfg_expert":
                mock_output = "The equipment is rated for 1600C."
                mock_sources = ["EQ-SPEC-01"]
            elif agent_id == "safety_expert":
                mock_output = "WARNING: Appropriate thermal PPE must be worn."
                mock_sources = ["SOP-SAFETY-99"]
                
            results.append({
                "step": node["step"],
                "agent_id": agent_id,
                "output": mock_output,
                "sources": mock_sources
            })
            
        return results
