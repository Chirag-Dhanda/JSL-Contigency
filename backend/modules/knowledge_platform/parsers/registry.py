"""Parser registry — auto-discovers and dispatches to the correct parser."""
import logging
from .base_parser import BaseParser
from .pdf_parser import PdfParser
from .docx_parser import DocxParser
from .text_parser import TextParser
from .json_csv_parser import JsonCsvParser
from .ocr_placeholder import OcrPlaceholderParser

logger = logging.getLogger("KnowledgePlatform.ParserRegistry")


class ParserRegistry:
    """
    Maintains a registry of file parsers keyed by extension.
    New parsers can be added via register_parser() without modifying platform code.
    """

    def __init__(self):
        self._parsers: dict[str, BaseParser] = {}
        # Register default parsers
        for parser in [PdfParser(), DocxParser(), TextParser(), JsonCsvParser(), OcrPlaceholderParser()]:
            for ext in parser.supported_extensions:
                self._parsers[ext.lower()] = parser
        logger.info(f"ParserRegistry initialized with {len(self._parsers)} extension mappings.")

    def register_parser(self, parser: BaseParser) -> None:
        """Register a custom parser. Overrides any existing parser for the same extension."""
        for ext in parser.supported_extensions:
            self._parsers[ext.lower()] = parser
            logger.info(f"Registered custom parser for extension '{ext}'.")

    def get_parser(self, filename: str) -> BaseParser:
        """Returns the appropriate parser for a given filename."""
        ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        parser = self._parsers.get(ext)
        if not parser:
            raise ValueError(f"No parser registered for file type '{ext}' (file: '{filename}').")
        return parser

    def parse(self, file_bytes: bytes, filename: str) -> str:
        """Convenience: get parser and execute parse in one call."""
        parser = self.get_parser(filename)
        return parser.parse(file_bytes, filename)

    @property
    def supported_extensions(self) -> list[str]:
        return list(self._parsers.keys())
