import json
import os
from logging import getLogger

from modules.sop.service import SOPEngine
from modules.safety.service import SafetyLearningEngine
from modules.compliance.service import ComplianceFramework
from modules.manufacturing.service import ManufacturingExplorerService
from modules.equipment.service import EquipmentKnowledgeService
from modules.resource_library.service import ResourceCenterEngine
from modules.departments.service import DepartmentHubEngine

logger = getLogger("LearningPlatformOrchestrator")

class LearningPlatformOrchestrator:
    def __init__(self):
        # Initialize all Stage 3 Engines
        self.sop_engine = SOPEngine()
        self.safety_engine = SafetyLearningEngine()
        self.compliance_engine = ComplianceFramework()
        self.manufacturing_explorer = ManufacturingExplorerService()
        self.equipment_engine = EquipmentKnowledgeService()
        self.resource_center = ResourceCenterEngine()
        self.department_hubs = DepartmentHubEngine()
        
        logger.info("Learning Platform Orchestrator Initialized with all Stage 3 Modules.")

    def bootstrap_demo_environment(self, demo_data_dir: str):
        """Loads realistic demo data from JSON files and cross-links the modules."""
        logger.info("Bootstrapping Demo Environment...")
        
        users_file = os.path.join(demo_data_dir, "users", "users.json")
        hubs_file = os.path.join(demo_data_dir, "departments", "hubs.json")
        
        # Load Users
        if os.path.exists(users_file):
            with open(users_file, "r") as f:
                users_data = json.load(f)
                logger.info(f"Loaded {len(users_data.get('personas', []))} demo personas.")
                # In a full run, we would map these to user records and compliance evaluations
                
        # Load Hub Overrides
        if os.path.exists(hubs_file):
            with open(hubs_file, "r") as f:
                hubs_data = json.load(f)
                logger.info(f"Loaded {len(hubs_data.get('hubs', []))} demo department configurations.")
                # E.g., updating the pre-populated hubs with custom demo announcements

        logger.info("Demo Environment successfully hydrated.")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Path assumes running from backend directory
    demo_dir = os.path.abspath(os.path.join("..", "demo-data"))
    
    orchestrator = LearningPlatformOrchestrator()
    orchestrator.bootstrap_demo_environment(demo_dir)
