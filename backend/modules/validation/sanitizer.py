import re
from logging import getLogger

logger = getLogger("Sanitizer")

class InputSanitizer:
    """Enterprise framework for scrubbing malicious input payloads."""
    
    # Matches common malicious HTML tags
    HTML_PATTERN = re.compile(r'<(script|iframe|object|embed|applet|style)[^>]*>.*?</\1>', re.IGNORECASE)
    
    # Matches common SQL injection keywords (very naive approach for demonstration)
    SQL_PATTERN = re.compile(r'\b(DROP|DELETE|UPDATE|INSERT|SELECT|UNION)\b', re.IGNORECASE)
    
    @classmethod
    def sanitize_string(cls, raw: str) -> str:
        if not raw:
            return raw
            
        original = raw
        
        # 1. Strip malicious HTML
        raw = cls.HTML_PATTERN.sub('[REMOVED]', raw)
        
        # 2. Escape standard HTML chars (XSS Prevention)
        raw = raw.replace("<", "&lt;").replace(">", "&gt;")
        
        # 3. Naive SQL injection strip
        raw = cls.SQL_PATTERN.sub('[REMOVED]', raw)
        
        if original != raw:
            logger.warning("Sanitizer intercepted and neutralized a potentially malicious payload.")
            
        return raw
