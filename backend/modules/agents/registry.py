import logging
from typing import Dict, List, Any
from pydantic import BaseModel, Field

logger = logging.getLogger("AgentRegistry")

class AgentManifest(BaseModel):
    agent_id: str
    name: str
    capabilities: List[str]
    version: str = "1.0"
    status: str = "Online"
    priority: int = 1

class AgentRegistry:
    """Maintains the directory of available specialized agents."""
    
    def __init__(self):
        self._agents: Dict[str, AgentManifest] = {
            "mfg_expert": AgentManifest(
                agent_id="mfg_expert",
                name="Manufacturing Expert",
                capabilities=["equipment_specs", "process_parameters"],
                priority=10
            ),
            "safety_expert": AgentManifest(
                agent_id="safety_expert",
                name="Safety Expert",
                capabilities=["ppe", "loto", "hazards"],
                priority=100  # Highest priority for conflict resolution
            )
        }

    def get_agent(self, agent_id: str) -> AgentManifest:
        return self._agents.get(agent_id)

    def list_agents(self) -> List[AgentManifest]:
        return list(self._agents.values())
