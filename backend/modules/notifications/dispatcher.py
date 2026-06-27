from typing import Dict
from logging import getLogger
from .models import NotificationMessage
from .enums import DeliveryChannel

logger = getLogger("NotificationDispatcher")

class BaseDispatcher:
    async def dispatch(self, message: NotificationMessage) -> bool:
        raise NotImplementedError

class InAppDispatcher(BaseDispatcher):
    async def dispatch(self, message: NotificationMessage) -> bool:
        logger.info(f"IN-APP Delivery to {message.recipient_id} | {message.subject}")
        return True

class EmailDispatcher(BaseDispatcher):
    async def dispatch(self, message: NotificationMessage) -> bool:
        logger.info(f"EMAIL Delivery to {message.recipient_id} | {message.subject}")
        return True

class DispatcherRegistry:
    def __init__(self):
        self._dispatchers: Dict[DeliveryChannel, BaseDispatcher] = {
            DeliveryChannel.IN_APP: InAppDispatcher(),
            DeliveryChannel.EMAIL: EmailDispatcher()
        }
        
    async def route(self, message: NotificationMessage, channel: DeliveryChannel) -> bool:
        dispatcher = self._dispatchers.get(channel)
        if dispatcher:
            return await dispatcher.dispatch(message)
        logger.warning(f"No dispatcher configured for {channel}")
        return False
