import logging

logger = logging.getLogger("DocumentClassifier")

class DocumentClassifier:
    """Evaluates content to automatically tag the document type."""
    
    def __init__(self):
        pass
        
    def classify(self, text: str) -> str:
        """
        Analyzes the text content (and future metadata) to classify the document.
        Returns a classification string.
        """
        logger.debug("Classifying document...")
        
        text_lower = text.lower()
        
        if "standard operating procedure" in text_lower or "sop" in text_lower:
            return "Standard Operating Procedure"
        elif "safety" in text_lower and "hazard" in text_lower:
            return "Safety Manual"
        elif "maintenance" in text_lower:
            return "Maintenance Procedure"
            
        return "Unclassified Document"
