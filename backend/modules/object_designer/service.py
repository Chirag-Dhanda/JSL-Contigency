import logging
from typing import Dict, List
from modules.object_definitions.templates import VisualObjectDefinition, get_equipment_template, get_sop_template
from modules.object_runtime.generator import RuntimeGeneratorService
from exceptions.base import NotFoundException

logger = logging.getLogger("ObjectDesigner")

class ObjectDesignerService:
    """
    Manages the lifecycle of Visual Object Definitions in the Knowledge Studio.
    Allows MASTER_EDITORS to save drafts of objects before compiling them.
    """
    
    def __init__(self, runtime_generator: RuntimeGeneratorService):
        self.runtime = runtime_generator
        # Mock database for visual blueprints
        self._blueprints: Dict[str, VisualObjectDefinition] = {}
        
        # Seed templates
        eq = get_equipment_template()
        sop = get_sop_template()
        self._blueprints[eq.id] = eq
        self._blueprints[sop.id] = sop
        
        logger.info("Object Designer Service Initialized.")
        
    def save_blueprint(self, blueprint: VisualObjectDefinition) -> VisualObjectDefinition:
        """Saves a draft of a visual object."""
        self._blueprints[blueprint.id] = blueprint
        logger.info(f"Saved Object Blueprint: {blueprint.display_name} ({blueprint.type_id})")
        return blueprint
        
    def get_blueprint(self, blueprint_id: str) -> VisualObjectDefinition:
        if blueprint_id not in self._blueprints:
            raise NotFoundException(message=f"Blueprint {blueprint_id} not found.")
        return self._blueprints[blueprint_id]
        
    def list_blueprints(self) -> List[VisualObjectDefinition]:
        return list(self._blueprints.values())
        
    def publish_blueprint(self, blueprint_id: str):
        """
        Takes a draft blueprint and compiles it via the Runtime Generator,
        making it instantly active in the Enterprise AI and Metadata systems.
        """
        blueprint = self.get_blueprint(blueprint_id)
        
        # Compile and register
        self.runtime.compile_and_register(blueprint)
        
        blueprint.status = "ACTIVE"
        logger.info(f"Blueprint {blueprint_id} published to runtime.")
        return blueprint
