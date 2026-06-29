"""OCR placeholder — raises NotImplementedError for image files.
Future implementation should integrate Tesseract or a cloud OCR API.
"""
from .base_parser import BaseParser


class OcrPlaceholderParser(BaseParser):
    @property
    def supported_extensions(self) -> list[str]:
        return [".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif", ".webp"]

    def parse(self, file_bytes: bytes, filename: str = "") -> str:
        raise NotImplementedError(
            f"OCR parsing is not yet implemented. File '{filename}' requires an OCR provider. "
            "Future implementation will integrate Tesseract or a cloud OCR service."
        )
