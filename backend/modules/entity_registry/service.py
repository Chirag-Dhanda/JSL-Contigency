import logging
from typing import Dict, List, Optional
from .models import EntityTypeDefinition
from exceptions.base import NotFoundException, SystemException

logger = logging.getLogger("EntityRegistry")

class EntityRegistryService:
    """
    Manages the active entity types available in the enterprise platform.
    Acts as the source of truth for dynamic schemas.
    """
    
    def __init__(self):
        # In-memory mock for Stage 5.1 (will transition to DB in Stage 5.x)
        self._types: Dict[str, EntityTypeDefinition] = {}
        logger.info("Entity Registry Initialized.")

    def register_type(self, definition: EntityTypeDefinition) -> EntityTypeDefinition:
        """Registers a new dynamic entity type."""
        if definition.type_id in self._types:
            raise SystemException(message=f"Entity Type '{definition.type_id}' is already registered.")
        
        self._types[definition.type_id] = definition
        logger.info(f"Registered new Entity Type: {definition.type_id}")
        return definition

    def get_type(self, type_id: str) -> EntityTypeDefinition:
        """Retrieves an entity type definition by ID."""
        if type_id not in self._types:
            raise NotFoundException(message=f"Entity Type '{type_id}' not found in registry.")
        return self._types[type_id]

    def list_types(self, active_only: bool = True) -> List[EntityTypeDefinition]:
        """Lists all registered entity types."""
        if active_only:
            return [t for t in self._types.values() if t.is_active]
        return list(self._types.values())

    def deactivate_type(self, type_id: str) -> EntityTypeDefinition:
        """Deactivates an entity type, preventing new entities from being created with it."""
        entity_type = self.get_type(type_id)
        entity_type.is_active = False
        logger.warning(f"Deactivated Entity Type: {type_id}")
        return entity_type
