from typing import Dict, Any
from exceptions.base import SystemException
from .models import MessageTemplate

class TemplateEngine:
    """Parses text templates and injects dynamic variables."""
    
    def __init__(self):
        # In-memory registry for functional testing
        self._registry: Dict[str, MessageTemplate] = {}
        
    def register_template(self, template: MessageTemplate):
        self._registry[template.template_id] = template
        
    def render(self, template_id: str, context: Dict[str, Any]) -> dict:
        """
        Returns a dict containing 'subject' and 'body'.
        Basic naive {{ key }} replacement for demonstration.
        """
        template = self._registry.get(template_id)
        if not template:
            raise SystemException(f"Template {template_id} not found.")
            
        subject = template.subject
        body = template.body_content
        
        for key, value in context.items():
            placeholder = f"{{{{ {key} }}}}"
            subject = subject.replace(placeholder, str(value))
            body = body.replace(placeholder, str(value))
            
        return {
            "subject": subject,
            "body": body,
            "supported_channels": template.supported_channels
        }
