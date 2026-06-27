from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

class ContextBlock(BaseModel):
    """Represents the user's current platform context."""
    current_page: str = Field(default="Home", description="The current UI route/page")
    current_lesson: Optional[str] = Field(default=None, description="Active learning lesson")
    current_sop: Optional[str] = Field(default=None, description="Active standard operating procedure")
    current_equipment: Optional[str] = Field(default=None, description="Equipment currently being viewed")
    manufacturing_stage: Optional[str] = Field(default=None, description="Current stage in the process")
    department: Optional[str] = Field(default=None, description="User's department context")
    user_role: str = Field(default="Employee", description="Role clearance level")
    workspace: Optional[str] = Field(default=None, description="Current workspace")

class MessageModel(BaseModel):
    """A single chat message."""
    id: str
    role: str
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ConversationModel(BaseModel):
    """A complete conversation session."""
    id: str
    title: str = "New Conversation"
    user_id: str
    is_pinned: bool = Field(default=False, description="Pinned for quick access")
    context_block: ContextBlock = Field(default_factory=ContextBlock)
    messages: List[MessageModel] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
