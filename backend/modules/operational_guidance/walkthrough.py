import logging
from typing import Dict, Any

logger = logging.getLogger("SOPWalkthroughManager")

class SOPWalkthroughManager:
    """A state-tracking framework holding the user's progress through a procedure."""
    
    def __init__(self):
        # In memory state map: user_id -> state
        self.active_walkthroughs: Dict[str, Dict[str, Any]] = {}

    def start_walkthrough(self, user_id: str, sop_id: str) -> Dict[str, Any]:
        logger.info(f"Starting Walkthrough for user {user_id} on {sop_id}")
        state = {
            "sop_id": sop_id,
            "current_step": 1,
            "total_steps": 10, # Mocked
            "checkpoints_cleared": []
        }
        self.active_walkthroughs[user_id] = state
        return state

    def next_step(self, user_id: str, confirm_checkpoint: bool = False) -> Dict[str, Any]:
        logger.debug(f"Advancing step for user {user_id}")
        if user_id in self.active_walkthroughs:
            state = self.active_walkthroughs[user_id]
            if confirm_checkpoint:
                state["checkpoints_cleared"].append(state["current_step"])
                
            if state["current_step"] < state["total_steps"]:
                state["current_step"] += 1
            return state
        return {"error": "No active walkthrough"}
