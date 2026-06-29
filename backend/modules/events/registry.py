"""
Event Schema Registry (EP-11).
Authoritative catalog of all registered event types and schema versions.
"""
import logging
from typing import Dict, List, Optional

from .models import EventSchema

logger = logging.getLogger("Event.Registry")


class EventRegistry:
    def __init__(self):
        # Key: event_type -> version -> EventSchema
        self._schemas: Dict[str, Dict[int, EventSchema]] = {}

    def register_schema(self, schema: EventSchema) -> None:
        if schema.event_type not in self._schemas:
            self._schemas[schema.event_type] = {}
        
        self._schemas[schema.event_type][schema.version] = schema
        logger.info(f"Registered schema for {schema.event_type} v{schema.version}")

    def get_schema(self, event_type: str, version: int = 1) -> Optional[EventSchema]:
        return self._schemas.get(event_type, {}).get(version)

    def validate_payload(self, event_type: str, version: int, payload: Dict) -> bool:
        """
        Validates a payload against the registered schema.
        For this mock, we just check if a schema exists.
        In a real app, this would use jsonschema.validate()
        """
        schema = self.get_schema(event_type, version)
        if not schema:
            logger.warning(f"Schema not found for {event_type} v{version}")
            return False
            
        # Mock validation always passes if schema is known
        return True

    def get_catalog(self) -> List[EventSchema]:
        """Returns the latest version of all registered schemas."""
        catalog = []
        for event_type, versions in self._schemas.items():
            latest_version = max(versions.keys())
            catalog.append(versions[latest_version])
        return catalog
