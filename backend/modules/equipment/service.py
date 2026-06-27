from typing import Dict, List, Optional
from logging import getLogger
import uuid

from .models import EquipmentKnowledge, EquipmentRelationship, AIHooks
from .enums import EquipmentStatus

logger = getLogger("EquipmentKnowledgeService")

class EquipmentKnowledgeService:
    def __init__(self):
        self._equipment: Dict[str, EquipmentKnowledge] = {}

    def register_equipment(self, equipment: EquipmentKnowledge):
        self._equipment[equipment.id] = equipment
        logger.info(f"Registered Equipment Knowledge: {equipment.name}")

    def get_equipment(self, equipment_id: str) -> Optional[EquipmentKnowledge]:
        return self._equipment.get(equipment_id)

    def search_equipment(self, query: str = "", department_id: Optional[str] = None) -> List[EquipmentKnowledge]:
        results = []
        for eq in self._equipment.values():
            if query and query.lower() not in eq.name.lower() and query.lower() not in eq.purpose.lower():
                continue
            if department_id and eq.department_id != department_id:
                continue
            results.append(eq)
        return results

    def resolve_relationships(self, equipment_id: str) -> Optional[EquipmentRelationship]:
        """Utility to fetch just the linked knowledge objects for an equipment piece."""
        eq = self.get_equipment(equipment_id)
        return eq.relationships if eq else None
