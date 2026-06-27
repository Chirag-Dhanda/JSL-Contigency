from core.module import BaseModule
from core.di import ServiceContainer
from .service import (
    OrganizationService, 
    DepartmentService, 
    RoleService, 
    ReportingService, 
    HierarchyService
)
from logging import getLogger

logger = getLogger("OrganizationModule")

class OrganizationModule(BaseModule):
    
    @property
    def name(self) -> str:
        return "Organization"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: ServiceContainer) -> None:
        """Register Organization Domain services into the global DI container."""
        logger.debug("Registering Organization Services...")
        
        container.register_singleton(OrganizationService, OrganizationService())
        container.register_singleton(DepartmentService, DepartmentService())
        container.register_singleton(RoleService, RoleService())
        container.register_singleton(ReportingService, ReportingService())
        container.register_singleton(HierarchyService, HierarchyService())

    async def initialize(self) -> None:
        logger.info("Organization Module Initialized.")

    async def shutdown(self) -> None:
        logger.info("Organization Module Shutdown.")
