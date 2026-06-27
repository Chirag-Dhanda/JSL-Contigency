from typing import Dict, List, Optional
from logging import getLogger
import uuid

from .models import LibraryItem, Collection

logger = getLogger("ContentLibraryService")

class ContentLibraryService:
    def __init__(self):
        self._library: Dict[str, LibraryItem] = {}
        self._collections: Dict[str, Collection] = {}

    def catalog_item(self, item: LibraryItem):
        """Adds a published LCMS item to the public searchable library."""
        self._library[item.id] = item
        logger.info(f"Cataloged {item.content_type.value}: {item.title}")

    def search(
        self, 
        query: str = "", 
        department: Optional[str] = None, 
        role: Optional[str] = None,
        equipment_id: Optional[str] = None,
        tags: List[str] = []
    ) -> List[LibraryItem]:
        """Core search architecture."""
        results = []
        for item in self._library.values():
            # Basic keyword match
            if query and query.lower() not in item.title.lower() and query.lower() not in item.description.lower():
                continue
                
            # Filter matches
            if department and department not in item.departments:
                continue
            if role and role not in item.role_ids:
                continue
            if equipment_id and equipment_id not in item.equipment_ids:
                continue
            if tags and not all(tag in item.tags for tag in tags):
                continue
                
            results.append(item)
            
        return results

    def create_collection(self, collection: Collection):
        self._collections[collection.id] = collection
        logger.info(f"Created collection: {collection.title}")
