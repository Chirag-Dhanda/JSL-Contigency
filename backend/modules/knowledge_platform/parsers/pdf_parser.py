"""PDF parser using pypdf."""
import io
from .base_parser import BaseParser


class PdfParser(BaseParser):
    @property
    def supported_extensions(self) -> list[str]:
        return [".pdf"]

    def parse(self, file_bytes: bytes, filename: str = "") -> str:
        try:
            from pypdf import PdfReader  # type: ignore
            reader = PdfReader(io.BytesIO(file_bytes))
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(pages).strip()
        except Exception as e:
            raise ValueError(f"PDF parse failed for '{filename}': {e}") from e
