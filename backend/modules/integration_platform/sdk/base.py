"""
Base SDK for Enterprise Connectors (EP-10).
"""
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any

from ..models import DataPayload

class ConnectorContext:
    """Context injected into connectors at runtime."""
    def __init__(self, config: Dict[str, Any], secrets: Dict[str, str], logger: logging.Logger):
        self.config = config
        self.secrets = secrets
        self.logger = logger


class BaseConnector(ABC):
    """
    Abstract Base Class for all external integrations.
    Vendor-specific logic goes into subclasses.
    """
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the integration provider (e.g., 'SAP', 'SCADA')."""
        pass

    @abstractmethod
    async def connect(self, context: ConnectorContext) -> bool:
        """Establish connection or validate credentials."""
        pass

    @abstractmethod
    async def health_check(self, context: ConnectorContext) -> bool:
        """Verify the external system is reachable."""
        pass

    @abstractmethod
    async def discover_schema(self, context: ConnectorContext) -> Dict[str, Any]:
        """Fetch external system schema metadata (for mapping UI)."""
        pass

    @abstractmethod
    async def read(self, context: ConnectorContext, query: Dict[str, Any]) -> List[DataPayload]:
        """Read data from the external system."""
        pass

    @abstractmethod
    async def write(self, context: ConnectorContext, payloads: List[DataPayload]) -> bool:
        """Write data back to the external system."""
        pass
