"""
Workflow Runtime Engine (EP-07).
Executes workflow instances via the state machine.
"""
import logging
import uuid
from typing import Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import DbWorkflowInstance, DbWorkflowAuditLog
from .models import WorkflowInstanceModel, WorkflowDefinitionMeta
from .definition import WorkflowDefinitionService

logger = logging.getLogger("WorkflowEngine.Runtime")


class WorkflowRuntimeEngine:
    def __init__(self, session_factory, definition_service: WorkflowDefinitionService):
        self.session_factory = session_factory
        self.definition_service = definition_service

    async def start_workflow(self, workflow_name: str, started_by: str, target_entity_id: Optional[str] = None, target_entity_type: Optional[str] = None) -> WorkflowInstanceModel:
        """Starts a new instance of the latest published workflow."""
        definition = await self.definition_service.get_published_version(workflow_name)
        if not definition:
            raise ValueError(f"No published workflow found for '{workflow_name}'")

        # Find Start Node
        start_state = next((s for s in definition.states if s.node_type == "START"), None)
        if not start_state:
            raise ValueError(f"Workflow '{workflow_name}' has no START state.")

        async with self.session_factory() as db:
            db_inst = DbWorkflowInstance(
                workflow_id=definition.id,
                target_entity_id=target_entity_id,
                target_entity_type=target_entity_type,
                status="RUNNING",
                current_state=start_state.id,
                started_by=started_by
            )
            db.add(db_inst)
            
            # Audit log
            audit = DbWorkflowAuditLog(
                instance_id=db_inst.id,
                action_type="WORKFLOW_STARTED",
                to_state=start_state.id,
                actor_id=started_by
            )
            db.add(audit)
            
            await db.commit()
            await db.refresh(db_inst)
            
            logger.info(f"Started instance {db_inst.id} for workflow '{workflow_name}'")
            return self._to_pydantic(db_inst)

    async def advance_state(self, instance_id: str, trigger_event: str, actor_id: str) -> WorkflowInstanceModel:
        """
        Evaluates transitions from the current state and advances if conditions are met.
        For EP-07, we assume the trigger_event matches a transition label.
        """
        async with self.session_factory() as db:
            stmt = select(DbWorkflowInstance).where(DbWorkflowInstance.id == instance_id)
            db_inst = (await db.execute(stmt)).scalar_one_or_none()
            if not db_inst or db_inst.status != "RUNNING":
                raise ValueError(f"Instance {instance_id} is not running.")
                
            # Need the definition to evaluate
            # (In reality, we'd cache this or load it via relationship)
            # Stubbed logic for EP-07:
            logger.info(f"Advancing state for {instance_id} triggered by {trigger_event}")
            
            # 1. Evaluate transitions
            # 2. Update current_state
            # 3. Fire Entry Actions for new state
            
            # For demonstration, we just log the audit and transition to a mock state
            old_state = db_inst.current_state
            db_inst.current_state = "NEXT_STATE_STUB"
            
            audit = DbWorkflowAuditLog(
                instance_id=db_inst.id,
                action_type="STATE_CHANGE",
                from_state=old_state,
                to_state=db_inst.current_state,
                actor_id=actor_id,
                details={"trigger": trigger_event}
            )
            db.add(audit)
            
            await db.commit()
            await db.refresh(db_inst)
            
            return self._to_pydantic(db_inst)

    def _to_pydantic(self, db_obj: DbWorkflowInstance) -> WorkflowInstanceModel:
        return WorkflowInstanceModel(
            id=db_obj.id,
            workflow_id=db_obj.workflow_id,
            target_entity_id=db_obj.target_entity_id,
            target_entity_type=db_obj.target_entity_type,
            status=db_obj.status,
            current_state=db_obj.current_state,
            context_data=db_obj.context_data,
            started_by=db_obj.started_by,
            created_at=db_obj.created_at,
            completed_at=db_obj.completed_at
        )
