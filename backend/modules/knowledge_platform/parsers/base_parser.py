"""Base parser interface — all parsers must implement this contract."""
from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Abstract base for all document parsers."""
    
    @property
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Return list of supported file extensions e.g. ['.pdf']."""
        ...

    @abstractmethod
    def parse(self, file_bytes: bytes, filename: str = "") -> str:
        """
        Parse raw file bytes into a plain-text string.
        Raises ValueError on unrecoverable parse failure.
        """
        ...
