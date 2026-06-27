from typing import Dict, List, Optional
from logging import getLogger
import uuid

from .models import SafetyModule, Hazard, PPEItem
from .enums import SafetyCategory

logger = getLogger("SafetyLearningEngine")

class SafetyLearningEngine:
    def __init__(self):
        self._modules: Dict[str, SafetyModule] = {}
        self._hazards: Dict[str, Hazard] = {}
        self._ppe_items: Dict[str, PPEItem] = {}

    def register_safety_module(self, module: SafetyModule):
        self._modules[module.id] = module
        logger.info(f"Registered Safety Module: {module.title}")

    def get_safety_module(self, module_id: str) -> Optional[SafetyModule]:
        return self._modules.get(module_id)

    def get_modules_by_category(self, category: SafetyCategory) -> List[SafetyModule]:
        return [mod for mod in self._modules.values() if mod.category == category]
        
    def register_hazard(self, hazard: Hazard):
        self._hazards[hazard.id] = hazard

    def get_hazard(self, hazard_id: str) -> Optional[Hazard]:
        return self._hazards.get(hazard_id)

    def register_ppe_item(self, ppe: PPEItem):
        self._ppe_items[ppe.id] = ppe

    def get_ppe_item(self, ppe_id: str) -> Optional[PPEItem]:
        return self._ppe_items.get(ppe_id)
