from typing import Any, Type, TypeVar, Dict, Callable
from exceptions.base import SystemException
from logging import getLogger
import threading

T = TypeVar('T')

logger = getLogger("ServiceContainer")

class ServiceContainer:
    """Enterprise Dependency Injection Container."""
    
    def __init__(self):
        self._singletons: Dict[Type, Any] = {}
        self._transient_factories: Dict[Type, Callable[..., Any]] = {}
        self._lock = threading.Lock()

    def register_singleton(self, interface: Type[T], implementation: T) -> None:
        """Registers a persistent singleton instance."""
        with self._lock:
            if interface in self._singletons or interface in self._transient_factories:
                logger.error(f"Duplicate registration attempted for {interface.__name__}")
                raise SystemException(f"Service {interface.__name__} is already registered.")
            self._singletons[interface] = implementation
            logger.trace(f"Registered Singleton: {interface.__name__}")

    def register_transient(self, interface: Type[T], factory: Callable[..., T]) -> None:
        """Registers a factory for generating transient instances on demand."""
        with self._lock:
            if interface in self._singletons or interface in self._transient_factories:
                logger.error(f"Duplicate registration attempted for {interface.__name__}")
                raise SystemException(f"Service {interface.__name__} is already registered.")
            self._transient_factories[interface] = factory
            logger.trace(f"Registered Transient Factory: {interface.__name__}")

    def resolve(self, interface: Type[T]) -> T:
        """Resolves a service from the container."""
        # Check singletons first
        if interface in self._singletons:
            return self._singletons[interface]
        
        # Check transient factories
        if interface in self._transient_factories:
            return self._transient_factories[interface]()
            
        logger.error(f"Resolution failed for {interface.__name__}")
        raise SystemException(f"Service {interface.__name__} has not been registered in the container.")

    def clear(self):
        """Clears the container (useful for testing or full reset)."""
        with self._lock:
            self._singletons.clear()
            self._transient_factories.clear()

# Global Container Instance
container = ServiceContainer()
