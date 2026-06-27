import logging
from typing import Dict, List
from .models import RelationshipTypeDefinition
from exceptions.base import NotFoundException, SystemException

logger = logging.getLogger("RelationshipRegistry")

class RelationshipRegistryService:
    """
    Acts as the source of truth for valid entity relationship types.
    """
    
    def __init__(self):
        # In-memory mock for Stage 5.2
        self._types: Dict[str, RelationshipTypeDefinition] = {}
        logger.info("Relationship Registry Initialized.")

    def register_type(self, definition: RelationshipTypeDefinition) -> RelationshipTypeDefinition:
        if definition.type_id in self._types:
            raise SystemException(message=f"Relationship Type '{definition.type_id}' is already registered.")
        
        self._types[definition.type_id] = definition
        logger.info(f"Registered new Relationship Type: {definition.type_id}")
        return definition

    def get_type(self, type_id: str) -> RelationshipTypeDefinition:
        if type_id not in self._types:
            raise NotFoundException(message=f"Relationship Type '{type_id}' not found.")
        return self._types[type_id]

    def list_types(self, active_only: bool = True) -> List[RelationshipTypeDefinition]:
        if active_only:
            return [t for t in self._types.values() if t.is_active]
        return list(self._types.values())
