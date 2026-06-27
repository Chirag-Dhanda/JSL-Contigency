from pydantic import BaseModel
from typing import List

class MessageTemplate(BaseModel):
    template_id: str
    subject: str
    body_content: str
    language: str = "en"
    supported_channels: List[str]
