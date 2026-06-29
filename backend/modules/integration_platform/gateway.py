"""
Integration Gateway (EP-10).
The central router for all enterprise integrations. No direct access to external systems
is permitted outside this gateway.
"""
import logging
from typing import Dict, List, Any, Optional
import asyncio

from .models import ConnectorDefinition, ConnectorStatus, DataPayload, IntegrationEvent
from .sdk.base import BaseConnector, ConnectorContext
from .connectors.sap_connector import SAPConnector

logger = logging.getLogger("Integration.Gateway")


class IntegrationGateway:
    def __init__(self):
        self._definitions: Dict[str, ConnectorDefinition] = {}
        # Simple registry mapping provider strings to connector classes
        self._connector_registry = {
            "SAP": SAPConnector
        }
        self._events: List[IntegrationEvent] = []

    def register_definition(self, definition: ConnectorDefinition) -> None:
        self._definitions[definition.connector_id] = definition
        logger.info(f"Registered connector definition: {definition.name} ({definition.provider})")

    def _get_connector_instance(self, connector_id: str) -> BaseConnector:
        definition = self._definitions.get(connector_id)
        if not definition:
            raise ValueError(f"Connector {connector_id} not found.")
            
        connector_class = self._connector_registry.get(definition.provider.upper())
        if not connector_class:
            raise ValueError(f"Provider {definition.provider} not supported.")
            
        return connector_class()

    def _build_context(self, definition: ConnectorDefinition) -> ConnectorContext:
        # In a real app, secrets would be pulled from a Vault
        secrets = {}
        return ConnectorContext(config=definition.config, secrets=secrets, logger=logger)

    def _log_event(self, event: IntegrationEvent) -> None:
        self._events.append(event)
        # Would also publish this to the Audit / Security monitor

    async def execute_read(self, connector_id: str, query: Dict[str, Any]) -> List[DataPayload]:
        """Execute a read operation against a connector."""
        definition = self._definitions.get(connector_id)
        if not definition:
            raise ValueError(f"Connector {connector_id} not found.")
            
        if definition.status != ConnectorStatus.ACTIVE:
            raise PermissionError(f"Connector {connector_id} is not ACTIVE.")
            
        if "READ" not in definition.capabilities:
            raise PermissionError(f"Connector {connector_id} lacks READ capability.")

        connector = self._get_connector_instance(connector_id)
        context = self._build_context(definition)
        
        event = IntegrationEvent(connector_id=connector_id, action="READ", status="PENDING")
        try:
            await connector.connect(context)
            results = await connector.read(context, query)
            event.status = "SUCCESS"
            event.records_processed = len(results)
            return results
        except Exception as e:
            event.status = "FAILED"
            event.error_message = str(e)
            logger.error(f"Read failed on {connector_id}: {e}")
            raise
        finally:
            self._log_event(event)

    async def execute_write(self, connector_id: str, payloads: List[DataPayload]) -> bool:
        """Execute a write operation against a connector."""
        definition = self._definitions.get(connector_id)
        if not definition:
            raise ValueError(f"Connector {connector_id} not found.")
            
        if definition.status != ConnectorStatus.ACTIVE:
            raise PermissionError(f"Connector {connector_id} is not ACTIVE.")
            
        if "WRITE" not in definition.capabilities:
            raise PermissionError(f"Connector {connector_id} lacks WRITE capability. Governance review required.")

        connector = self._get_connector_instance(connector_id)
        context = self._build_context(definition)
        
        event = IntegrationEvent(connector_id=connector_id, action="WRITE", status="PENDING")
        try:
            await connector.connect(context)
            success = await connector.write(context, payloads)
            event.status = "SUCCESS" if success else "FAILED"
            event.records_processed = len(payloads) if success else 0
            return success
        except Exception as e:
            event.status = "FAILED"
            event.error_message = str(e)
            logger.error(f"Write failed on {connector_id}: {e}")
            raise
        finally:
            self._log_event(event)

    async def discover_schema(self, connector_id: str) -> Dict[str, Any]:
        """Discover schema from the external system."""
        definition = self._definitions.get(connector_id)
        if not definition:
            raise ValueError(f"Connector {connector_id} not found.")
            
        connector = self._get_connector_instance(connector_id)
        context = self._build_context(definition)
        
        await connector.connect(context)
        return await connector.discover_schema(context)

    def get_events(self, connector_id: Optional[str] = None) -> List[IntegrationEvent]:
        if connector_id:
            return [e for e in self._events if e.connector_id == connector_id]
        return self._events
