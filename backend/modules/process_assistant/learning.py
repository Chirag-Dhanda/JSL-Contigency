import logging

logger = logging.getLogger("LearningAssistant")

class LearningAssistant:
    """Assistant for adjusting explanation tone based on user role (Beginner vs Engineer)."""
    
    def __init__(self):
        pass

    def explain(self, concept: str, user_role: str) -> str:
        logger.debug(f"Explaining {concept} to role {user_role}")
        if user_role.lower() == "beginner":
            return f"Think of {concept} like a giant oven..."
        else:
            return f"The {concept} operates using electromagnetic induction..."
