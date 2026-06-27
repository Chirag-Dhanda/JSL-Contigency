import logging

logger = logging.getLogger("EquipmentExpert")

class EquipmentExpert:
    """Expert agent for detailing working principles, components, and maintenance."""
    
    def __init__(self):
        pass

    def explain_equipment(self, equipment_name: str, context: dict) -> str:
        logger.debug(f"Explaining equipment: {equipment_name}")
        return f"The {equipment_name} is designed to..."
