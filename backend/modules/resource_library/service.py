from typing import Dict, List, Optional
from logging import getLogger
import uuid

from .models import ResourceAsset, UserResourceInteraction
from .enums import ResourceType

logger = getLogger("ResourceCenterEngine")

class ResourceCenterEngine:
    def __init__(self):
        self._resources: Dict[str, ResourceAsset] = {}
        self._user_interactions: Dict[str, UserResourceInteraction] = {}

    def catalog_resource(self, resource: ResourceAsset):
        self._resources[resource.id] = resource
        logger.info(f"Cataloged resource: {resource.title}")

    def get_resource(self, resource_id: str) -> Optional[ResourceAsset]:
        return self._resources.get(resource_id)

    def search_resources(self, 
                         keyword: str = "", 
                         department_id: Optional[str] = None,
                         resource_type: Optional[ResourceType] = None,
                         equipment_id: Optional[str] = None) -> List[ResourceAsset]:
        results = []
        for res in self._resources.values():
            if keyword and keyword.lower() not in res.title.lower() and keyword.lower() not in res.description.lower():
                continue
            if department_id and res.department_id != department_id:
                continue
            if resource_type and res.resource_type != resource_type:
                continue
            if equipment_id and equipment_id not in res.relationships.equipment_ids:
                continue
            
            results.append(res)
        return results

    def get_user_interactions(self, user_id: str) -> UserResourceInteraction:
        if user_id not in self._user_interactions:
            self._user_interactions[user_id] = UserResourceInteraction(user_id=user_id)
        return self._user_interactions[user_id]
        
    def add_favorite(self, user_id: str, resource_id: str):
        interaction = self.get_user_interactions(user_id)
        if resource_id not in interaction.favorite_resource_ids:
            interaction.favorite_resource_ids.append(resource_id)
