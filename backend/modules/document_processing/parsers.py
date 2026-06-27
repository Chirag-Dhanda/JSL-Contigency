import abc
from .cleaner import ContentCleaner

class BaseParser(abc.ABC):
    """Abstract interface for extracting text from files."""
    
    def __init__(self):
        self.cleaner = ContentCleaner()
        
    @abc.abstractmethod
    def parse(self, file_path: str) -> str:
        pass

class PDFParser(BaseParser):
    def parse(self, file_path: str) -> str:
        """
        Extracts text from PDFs.
        If it detects 0 characters (scanned image), it would call the OCREngine.
        """
        # Mock extraction
        raw_text = "This is raw PDF text.   \n\n Page 1 of 5 \n  End."
        return self.cleaner.clean_text(raw_text)

class MarkdownParser(BaseParser):
    def parse(self, file_path: str) -> str:
        """Reads Markdown text directly."""
        # For mock test avoiding FileNotFoundError
        raw_text = "Mock Markdown Content"
        return self.cleaner.clean_text(raw_text)

class DOCXParser(BaseParser):
    def parse(self, file_path: str) -> str:
        """Extracts text and tables from Word documents."""
        return "Mock DOCX Content"

class PPTXParser(BaseParser):
    def parse(self, file_path: str) -> str:
        """Extracts text from PowerPoint slides and notes."""
        return "Mock PPTX Content"

class HTMLParser(BaseParser):
    def parse(self, file_path: str) -> str:
        """Extracts text from web pages or HTML documents."""
        return "Mock HTML Content"

class MediaParser(BaseParser):
    def parse(self, file_path: str) -> str:
        """Future framework for processing Audio and Video transcripts."""
        return "Media processing not yet implemented."
