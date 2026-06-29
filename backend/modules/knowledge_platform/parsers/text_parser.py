"""Plain text and Markdown parser."""
from .base_parser import BaseParser


class TextParser(BaseParser):
    @property
    def supported_extensions(self) -> list[str]:
        return [".txt", ".md", ".markdown", ".rst", ".log"]

    def parse(self, file_bytes: bytes, filename: str = "") -> str:
        try:
            # Try UTF-8 first, fall back to latin-1
            try:
                return file_bytes.decode("utf-8").strip()
            except UnicodeDecodeError:
                return file_bytes.decode("latin-1").strip()
        except Exception as e:
            raise ValueError(f"Text parse failed for '{filename}': {e}") from e
