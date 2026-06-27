import logging
import uuid
import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger("ConversationManager")

class ConversationManager:
    """Manages chat histories, message metadata, and session context."""
    
    def __init__(self):
        # In-memory store for now. Future: DB backed.
        self.conversations: Dict[str, Dict[str, Any]] = {}

    def start_conversation(self, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Starts a new conversation session."""
        conv_id = str(uuid.uuid4())
        self.conversations[conv_id] = {
            "id": conv_id,
            "user_id": user_id,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "metadata": metadata or {},
            "messages": []
        }
        logger.debug(f"Started conversation {conv_id} for user {user_id}")
        return conv_id

    def add_message(self, conv_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Appends a message to the conversation history."""
        if conv_id not in self.conversations:
            logger.warning(f"Attempted to add message to non-existent conversation {conv_id}")
            return
            
        message = {
            "id": str(uuid.uuid4()),
            "role": role,
            "content": content,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        self.conversations[conv_id]["messages"].append(message)
        logger.debug(f"Added {role} message to conversation {conv_id}")

    def get_history(self, conv_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves recent conversation history."""
        if conv_id not in self.conversations:
            return []
        
        # Return last N messages, excluding potentially very old ones to save context window
        return self.conversations[conv_id]["messages"][-limit:]

    def format_history_for_prompt(self, conv_id: str, limit: int = 10) -> str:
        """Formats the history into a string for injection into the prompt."""
        history = self.get_history(conv_id, limit)
        if not history:
            return ""
            
        parts = ["Conversation History:"]
        for msg in history:
            role = msg["role"].capitalize()
            parts.append(f"{role}: {msg['content']}")
            
        return "\n".join(parts)

    def rename_conversation(self, conv_id: str, user_id: str, new_title: str) -> bool:
        if conv_id in self.conversations and self.conversations[conv_id]["user_id"] == user_id:
            self.conversations[conv_id]["title"] = new_title
            return True
        return False

    def pin_conversation(self, conv_id: str, user_id: str, pin_status: bool) -> bool:
        if conv_id in self.conversations and self.conversations[conv_id]["user_id"] == user_id:
            self.conversations[conv_id]["is_pinned"] = pin_status
            return True
        return False

    def delete_conversation(self, conv_id: str, user_id: str) -> bool:
        if conv_id in self.conversations and self.conversations[conv_id]["user_id"] == user_id:
            del self.conversations[conv_id]
            logger.info(f"Deleted conversation {conv_id}")
            return True
        return False

    def summarize_conversation(self, conv_id: str) -> str:
        """Future: Generate a summary of the conversation to save context window."""
        return "Conversation summary not implemented yet."

conversation_manager = ConversationManager()
