import logging
from modules.conversations.manager import conversation_manager
from modules.conversations.models import ConversationModel

logging.basicConfig(level=logging.DEBUG)

def test_conversations():
    print("--- Testing Conversation Manager Extensions ---")
    user_id = "user-abc-123"
    
    # 1. Start Conversation
    conv_id = conversation_manager.start_conversation(user_id)
    print(f"Started Conversation: {conv_id}")
    
    # 2. Rename Conversation
    rename_success = conversation_manager.rename_conversation(conv_id, user_id, "EAF SOP Analysis")
    print(f"Renamed Conversation? {rename_success}")
    if rename_success:
        print(f"New Title: {conversation_manager.conversations[conv_id]['title']}")
        
    # 3. Pin Conversation
    pin_success = conversation_manager.pin_conversation(conv_id, user_id, True)
    print(f"Pinned Conversation? {pin_success}")
    if pin_success:
        print(f"Is Pinned: {conversation_manager.conversations[conv_id]['is_pinned']}")
        
    # 4. Fail Security Check (Wrong User)
    fail_rename = conversation_manager.rename_conversation(conv_id, "hacker-999", "Hacked Title")
    print(f"Unauthorized Rename Successful? {fail_rename}")
    
    # 5. Delete Conversation
    del_success = conversation_manager.delete_conversation(conv_id, user_id)
    print(f"Deleted Conversation? {del_success}")
    
    print("\nTest Complete!")

if __name__ == "__main__":
    test_conversations()
