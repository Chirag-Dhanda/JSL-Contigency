import logging
import uuid
from typing import Dict, Any, Optional

from .models import ConversationModel, ContextBlock, MessageModel
from .manager import conversation_manager

logger = logging.getLogger("ConversationService")

class ConversationService:
    """
    Service layer for Conversation Management, wrapping the basic manager 
    with domain models and Copilot-specific context tracking.
    """
    
    def __init__(self):
        # We will wrap the underlying dicts from manager.py into our Pydantic models when needed,
        # or upgrade the store directly. For now, we enhance the in-memory store.
        self._store: Dict[str, ConversationModel] = {}

    def create_conversation(self, user_id: str, context: Optional[ContextBlock] = None) -> ConversationModel:
        """Initializes a new Copilot session with context."""
        conv_id = str(uuid.uuid4())
        
        conv = ConversationModel(
            id=conv_id,
            user_id=user_id,
            context_block=context or ContextBlock()
        )
        self._store[conv_id] = conv
        logger.info(f"Created Copilot conversation {conv_id} for user {user_id}")
        return conv

    def get_conversation(self, conv_id: str) -> Optional[ConversationModel]:
        """Retrieves a conversation."""
        return self._store.get(conv_id)

    def update_context(self, conv_id: str, new_context: ContextBlock) -> bool:
        """Updates the context block as the user navigates the platform."""
        conv = self.get_conversation(conv_id)
        if not conv:
            return False
            
        conv.context_block = new_context
        # We can inject a system message into history if the context shifted dramatically, 
        # but for now we just update the live block.
        logger.debug(f"Updated context for conversation {conv_id}")
        return True

    def add_message(self, conv_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> Optional[MessageModel]:
        """Adds a message and updates the timestamp."""
        conv = self.get_conversation(conv_id)
        if not conv:
            return None
            
        msg = MessageModel(
            id=str(uuid.uuid4()),
            role=role,
            content=content,
            metadata=metadata or {}
        )
        conv.messages.append(msg)
        conv.updated_at = msg.timestamp
        
        # Also sync to the old manager if other systems rely on it
        conversation_manager.add_message(conv_id, role, content, metadata)
        
        return msg

    def delete_conversation(self, conv_id: str) -> bool:
        """Deletes a conversation."""
        if conv_id in self._store:
            del self._store[conv_id]
            logger.info(f"Deleted conversation {conv_id}")
            return True
        return False

conversation_service = ConversationService()
