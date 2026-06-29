"""DOCX parser using python-docx."""
import io
from .base_parser import BaseParser


class DocxParser(BaseParser):
    @property
    def supported_extensions(self) -> list[str]:
        return [".docx", ".doc"]

    def parse(self, file_bytes: bytes, filename: str = "") -> str:
        try:
            from docx import Document  # type: ignore
            doc = Document(io.BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n".join(paragraphs).strip()
        except Exception as e:
            raise ValueError(f"DOCX parse failed for '{filename}': {e}") from e
