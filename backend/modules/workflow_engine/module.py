"""
DI Registration for Enterprise Workflow & Process Orchestration Engine (EP-07).
"""
import logging
from typing import Any

from core.module import BaseModule
from core.di import container

from .definition import WorkflowDefinitionService
from .runtime import WorkflowRuntimeEngine
from .task_engine import TaskManagementService
from .approval_engine import ApprovalEngineService
from .events import EventEngine
from .notifications import NotificationInbox, NotificationFramework

logger = logging.getLogger("WorkflowEngineModule")


class WorkflowEngineModule(BaseModule):
    """Initializes and registers all components for the Enterprise Workflow Engine."""

    @property
    def name(self) -> str:
        return "WorkflowEngine"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: Any) -> None:
        logger.info("Registering Workflow Engine (EP-07) services...")

        # Resolve session factory from DB module
        from database.engine import get_async_session as session_factory

        # Event Bus (singleton so all modules share the same instance)
        event_engine = EventEngine()
        container.register_singleton(EventEngine, event_engine)

        # Notification Inbox + Framework (wires itself to the event bus)
        inbox = NotificationInbox()
        container.register_singleton(NotificationInbox, inbox)

        notif_framework = NotificationFramework(inbox=inbox, event_engine=event_engine)
        container.register_singleton(NotificationFramework, notif_framework)

        # Workflow Definition Service
        definition_svc = WorkflowDefinitionService(session_factory=session_factory)
        container.register_singleton(WorkflowDefinitionService, definition_svc)

        # Workflow Runtime Engine
        runtime = WorkflowRuntimeEngine(session_factory=session_factory, definition_service=definition_svc)
        container.register_singleton(WorkflowRuntimeEngine, runtime)

        # Task Management
        task_svc = TaskManagementService(session_factory=session_factory)
        container.register_singleton(TaskManagementService, task_svc)

        # Approval Engine
        approval_svc = ApprovalEngineService(session_factory=session_factory)
        container.register_singleton(ApprovalEngineService, approval_svc)

    async def initialize(self) -> None:
        logger.info("Workflow Engine initialized.")

    async def shutdown(self) -> None:
        pass
