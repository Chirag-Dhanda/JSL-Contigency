import os
import mimetypes

class DocumentValidator:
    """Validates files prior to entering the heavy extraction pipeline."""
    
    ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.pptx', '.xlsx', '.txt', '.md', '.html', '.csv', '.png', '.jpg'}
    MAX_FILE_SIZE_MB = 50
    
    @classmethod
    def validate_file(cls, file_path: str) -> bool:
        """
        Runs validation checks. In reality, this takes a file object or temp path.
        """
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in cls.ALLOWED_EXTENSIONS:
            raise ValueError(f"Extension {ext} is not supported for AI Ingestion.")
            
        # size check placeholder
        # if file_size > cls.MAX_FILE_SIZE_MB * 1024 * 1024:
        #    raise ValueError("File exceeds maximum allowed size.")
            
        # mime type check placeholder
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
             # Just a warning, not a hard fail
             pass
             
        return True
