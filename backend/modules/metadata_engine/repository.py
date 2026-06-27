from typing import Dict, List, Optional
from exceptions.base import NotFoundException
from modules.entity_registry.models import EntityTypeDefinition
from modules.entity_framework.models import EnterpriseEntity

class MetadataRepository:
    """
    In-memory persistence layer for Metadata Templates (Types) and Objects (Entities).
    This cleanly separates persistence from business logic.
    """
    def __init__(self):
        self._types: Dict[str, EntityTypeDefinition] = {}
        self._objects: Dict[str, EnterpriseEntity] = {}

    # --- TYPES / TEMPLATES ---
    def save_type(self, type_def: EntityTypeDefinition) -> EntityTypeDefinition:
        self._types[type_def.type_id] = type_def
        return type_def

    def get_type(self, type_id: str) -> EntityTypeDefinition:
        if type_id not in self._types:
            raise NotFoundException(message=f"Metadata Type '{type_id}' not found.")
        return self._types[type_id]

    def list_types(self) -> List[EntityTypeDefinition]:
        return list(self._types.values())

    def delete_type(self, type_id: str) -> bool:
        if type_id in self._types:
            del self._types[type_id]
            return True
        return False

    # --- OBJECTS / ENTITIES ---
    def save_object(self, entity: EnterpriseEntity) -> EnterpriseEntity:
        self._objects[entity.id] = entity
        return entity

    def get_object(self, object_id: str) -> EnterpriseEntity:
        if object_id not in self._objects:
            raise NotFoundException(message=f"Metadata Object '{object_id}' not found.")
        return self._objects[object_id]
        
    def list_objects(self, type_id: Optional[str] = None) -> List[EnterpriseEntity]:
        if type_id:
            return [obj for obj in self._objects.values() if obj.entity_type == type_id]
        return list(self._objects.values())

    def search_objects(self, query: str) -> List[EnterpriseEntity]:
        # Basic keyword search on name and display_name
        query = query.lower()
        results = []
        for obj in self._objects.values():
            if query in obj.name.lower() or query in obj.display_name.lower():
                results.append(obj)
        return results
