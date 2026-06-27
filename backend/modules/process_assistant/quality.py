import logging

logger = logging.getLogger("QualityAssistant")

class QualityAssistant:
    """Assistant for inspection guidance and defect explanations."""
    
    def __init__(self):
        pass

    def explain_quality_parameter(self, parameter: str) -> str:
        logger.debug(f"Explaining quality parameter: {parameter}")
        return f"The parameter {parameter} must be within the specified tolerances because..."
