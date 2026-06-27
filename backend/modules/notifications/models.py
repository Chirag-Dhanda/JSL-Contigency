from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
from .enums import NotificationType, DeliveryChannel, Priority, NotificationStatus

class NotificationMessage(BaseModel):
    id: str
    recipient_id: str
    type: NotificationType
    priority: Priority
    subject: str
    body: str
    channels: List[DeliveryChannel]
    status: NotificationStatus
    created_at: datetime
    delivered_at: datetime = None

class NotificationPreference(BaseModel):
    user_id: str
    disabled_channels: List[DeliveryChannel] = []
    quiet_hours_start: int = None # 0-23
    quiet_hours_end: int = None # 0-23
