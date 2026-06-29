"""
Approval Engine for Enterprise Workflow (EP-07).
Evaluates complex approvals (e.g. parallel, sequential).
"""
import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import DbWorkflowApproval, DbWorkflowAuditLog
from .models import WorkflowApprovalModel

logger = logging.getLogger("WorkflowEngine.ApprovalEngine")


class ApprovalEngineService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def request_approval(self, instance_id: str, approver_id: str, approver_department: str) -> WorkflowApprovalModel:
        async with self.session_factory() as db:
            db_approval = DbWorkflowApproval(
                instance_id=instance_id,
                approver_id=approver_id,
                approver_department=approver_department,
                status="PENDING"
            )
            db.add(db_approval)
            
            audit = DbWorkflowAuditLog(
                instance_id=instance_id,
                action_type="APPROVAL_REQUESTED",
                actor_id="SYSTEM",
                details={"approver": approver_id, "department": approver_department}
            )
            db.add(audit)
            
            await db.commit()
            await db.refresh(db_approval)
            return self._to_pydantic(db_approval)

    async def record_decision(self, approval_id: str, actor_id: str, decision: str, comments: Optional[str] = None) -> WorkflowApprovalModel:
        if decision not in ["APPROVED", "REJECTED"]:
            raise ValueError("Decision must be APPROVED or REJECTED")
            
        async with self.session_factory() as db:
            stmt = select(DbWorkflowApproval).where(DbWorkflowApproval.id == approval_id)
            db_approval = (await db.execute(stmt)).scalar_one_or_none()
            if not db_approval:
                raise ValueError("Approval request not found.")
                
            db_approval.status = decision
            db_approval.comments = comments
            
            audit = DbWorkflowAuditLog(
                instance_id=db_approval.instance_id,
                action_type=f"APPROVAL_{decision}",
                actor_id=actor_id,
                details={"comments": comments}
            )
            db.add(audit)
            
            await db.commit()
            await db.refresh(db_approval)
            return self._to_pydantic(db_approval)

    def _to_pydantic(self, db_obj: DbWorkflowApproval) -> WorkflowApprovalModel:
        return WorkflowApprovalModel(
            id=db_obj.id,
            instance_id=db_obj.instance_id,
            task_id=db_obj.task_id,
            status=db_obj.status,
            approver_id=db_obj.approver_id,
            approver_department=db_obj.approver_department,
            comments=db_obj.comments
        )
