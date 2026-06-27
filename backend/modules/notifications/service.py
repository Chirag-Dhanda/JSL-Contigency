from typing import Dict, Any
from datetime import datetime, timezone
import uuid
from .models import NotificationMessage, NotificationPreference
from .enums import NotificationType, Priority, DeliveryChannel, NotificationStatus
from .dispatcher import DispatcherRegistry
from modules.templates.engine import TemplateEngine
from logging import getLogger

logger = getLogger("NotificationService")

class NotificationService:
    def __init__(self, templates: TemplateEngine, dispatchers: DispatcherRegistry):
        self._templates = templates
        self._dispatchers = dispatchers
        
    async def send_notification(self, recipient_id: str, template_id: str, context: Dict[str, Any], priority: Priority = Priority.NORMAL):
        # 1. Render Template
        rendered = self._templates.render(template_id, context)
        
        # 2. Evaluate Preferences (Mocked logic)
        pref = NotificationPreference(user_id=recipient_id) # In reality, fetched from DB
        
        target_channels = []
        for ch_str in rendered["supported_channels"]:
            ch = DeliveryChannel(ch_str)
            if ch not in pref.disabled_channels:
                target_channels.append(ch)
                
        if not target_channels:
            logger.info(f"Notification aborted: User {recipient_id} has muted all supported channels.")
            return
            
        # 3. Create Entity
        msg = NotificationMessage(
            id=str(uuid.uuid4()),
            recipient_id=recipient_id,
            type=NotificationType.SYSTEM,
            priority=priority,
            subject=rendered["subject"],
            body=rendered["body"],
            channels=target_channels,
            status=NotificationStatus.QUEUED,
            created_at=datetime.now(timezone.utc)
        )
        
        # 4. Dispatch
        for channel in target_channels:
            success = await self._dispatchers.route(msg, channel)
            if success:
                msg.status = NotificationStatus.DELIVERED
                msg.delivered_at = datetime.now(timezone.utc)
