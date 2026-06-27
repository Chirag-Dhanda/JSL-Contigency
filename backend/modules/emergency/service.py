from typing import Dict, List, Optional
from logging import getLogger
import uuid

from .models import EmergencyProcedure
from .enums import EmergencyType

logger = getLogger("EmergencyResponseEngine")

class EmergencyResponseEngine:
    def __init__(self):
        self._procedures: Dict[str, EmergencyProcedure] = {}

    def register_procedure(self, procedure: EmergencyProcedure):
        self._procedures[procedure.id] = procedure
        logger.info(f"Registered Emergency Procedure: {procedure.title}")

    def get_procedure(self, procedure_id: str) -> Optional[EmergencyProcedure]:
        return self._procedures.get(procedure_id)

    def get_procedures_by_type(self, emergency_type: EmergencyType) -> List[EmergencyProcedure]:
        return [p for p in self._procedures.values() if p.type == emergency_type]
