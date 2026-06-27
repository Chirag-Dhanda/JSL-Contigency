import logging

logger = logging.getLogger("ProcessExpert")

class ProcessExpert:
    """Expert agent for explaining material flows, inputs, and operating sequences."""
    
    def __init__(self):
        pass

    def explain_process(self, process_name: str, context: dict) -> str:
        logger.debug(f"Explaining process: {process_name}")
        return f"The {process_name} process involves taking raw materials and..."
