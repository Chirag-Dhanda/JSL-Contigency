from typing import Dict, List, Optional
from logging import getLogger
import uuid

from .models import DepartmentHub, DepartmentLandingPage
from .enums import DepartmentType

logger = getLogger("DepartmentHubEngine")

class DepartmentHubEngine:
    def __init__(self):
        self._hubs: Dict[DepartmentType, DepartmentHub] = {}
        self._initialize_default_hubs()

    def _initialize_default_hubs(self):
        """Mock population of the requested default departments."""
        for dept_type in DepartmentType:
            name = dept_type.value.replace("_", " ").title()
            
            landing_page = DepartmentLandingPage(
                department_type=dept_type,
                mission=f"Default mission statement for {name}.",
                responsibilities=[f"Manage {name} operations."]
            )
            
            hub = DepartmentHub(
                id=str(uuid.uuid4()),
                department_type=dept_type,
                name=name,
                landing_page=landing_page
            )
            self._hubs[dept_type] = hub
            logger.debug(f"Initialized Department Hub: {name}")

    def get_hub(self, department_type: DepartmentType) -> Optional[DepartmentHub]:
        return self._hubs.get(department_type)
        
    def get_all_hubs(self) -> List[DepartmentHub]:
        return list(self._hubs.values())
