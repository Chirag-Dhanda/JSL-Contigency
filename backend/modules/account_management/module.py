from core.module import BaseModule
from core.di import ServiceContainer
from .service import AccountProvisioningService, ApprovalWorkflowService
from logging import getLogger

logger = getLogger("AccountManagementModule")

class AccountManagementModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "AccountManagement"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        logger.debug("Registering Account Management Services...")
        container.register_singleton(AccountProvisioningService, AccountProvisioningService())
        container.register_singleton(ApprovalWorkflowService, ApprovalWorkflowService())

    async def initialize(self) -> None:
        logger.info("Account Management Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Account Management Module Shutdown.")
