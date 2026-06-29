"""
Conversation Engine (EP-08).
Manages persistent, multi-turn enterprise AI conversations.
In-process storage for EP-08. DB persistence in EP-09.
"""
import logging
from typing import Dict, Optional, List

from .models import Conversation, ConversationTurn

logger = logging.getLogger("AIPlatform.Conversation")


class ConversationService:
    """
    In-process conversation store.
    Future: replaced by DbConversation / DbConversationTurn persistence.
    """

    def __init__(self):
        self._conversations: Dict[str, Conversation] = {}

    def create(self, user_id: str, linked_entity_id: Optional[str] = None, linked_workflow_id: Optional[str] = None) -> Conversation:
        conv = Conversation(
            user_id=user_id,
            linked_entity_id=linked_entity_id,
            linked_workflow_id=linked_workflow_id
        )
        self._conversations[conv.conversation_id] = conv
        logger.info(f"Created conversation {conv.conversation_id} for user {user_id}")
        return conv

    def get(self, conversation_id: str) -> Optional[Conversation]:
        return self._conversations.get(conversation_id)

    def get_or_create(self, conversation_id: Optional[str], user_id: str) -> Conversation:
        if conversation_id:
            conv = self.get(conversation_id)
            if conv:
                return conv
        return self.create(user_id)

    def append_turn(self, conversation_id: str, turn: ConversationTurn) -> None:
        conv = self._conversations.get(conversation_id)
        if conv:
            conv.turns.append(turn)
            from datetime import datetime, timezone
            conv.updated_at = datetime.now(timezone.utc)

    def get_history(self, conversation_id: str, last_n: int = 10) -> List[ConversationTurn]:
        conv = self._conversations.get(conversation_id)
        if not conv:
            return []
        return conv.turns[-last_n:]

    def list_for_user(self, user_id: str) -> List[Conversation]:
        return [c for c in self._conversations.values() if c.user_id == user_id]
