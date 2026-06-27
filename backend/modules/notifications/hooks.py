from logging import getLogger
from typing import Dict, Any

logger = getLogger("NotificationHooks")

class NotificationHooks:
    """Placeholder framework for future email/Teams integrations."""
    
    @classmethod
    async def on_access_request_created(cls, request_id: str, requester_id: str) -> None:
        logger.info(f"NOTIFICATION FIRED: Access Request {request_id} created by {requester_id}. (Awaiting Manager Approval)")
        
    @classmethod
    async def on_access_request_approved(cls, request_id: str, approver_id: str) -> None:
        logger.info(f"NOTIFICATION FIRED: Access Request {request_id} APPROVED by {approver_id}.")
        
    @classmethod
    async def on_access_request_rejected(cls, request_id: str, rejector_id: str) -> None:
        logger.info(f"NOTIFICATION FIRED: Access Request {request_id} REJECTED by {rejector_id}.")
