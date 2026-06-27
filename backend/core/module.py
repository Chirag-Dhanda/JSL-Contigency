from abc import ABC, abstractmethod
from typing import Dict, Any, Callable
from core.di import ServiceContainer
from logging import getLogger

class BaseModule(ABC):
    """Abstract base class for all enterprise modules (Auth, SAP, AI, etc.)"""
    
    def __init__(self):
        self.logger = getLogger(f"Module.{self.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        """The internal name of the module."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """The version of the module."""
        pass

    @abstractmethod
    def register_services(self, container: ServiceContainer) -> None:
        """Register any singleton or transient services into the IoC container."""
        pass
        
    @abstractmethod
    async def initialize(self) -> None:
        """Perform asynchronous initialization (e.g. connecting to DB, cache)."""
        pass
        
    @abstractmethod
    async def shutdown(self) -> None:
        """Perform graceful shutdown (e.g. closing connections)."""
        pass

    def register_health_checks(self) -> Dict[str, Callable[[], bool]]:
        """Optional: Return a dictionary of health check functions for this module."""
        return {}
