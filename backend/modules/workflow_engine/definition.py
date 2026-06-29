"""
Workflow Definition Service (EP-07).
Manages CRUD and versioning for workflow templates.
"""
import logging
from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import DbWorkflowDefinition
from .models import WorkflowDefinitionMeta

logger = logging.getLogger("WorkflowEngine.Definition")


class WorkflowDefinitionService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def create_draft(self, name: str, definition_payload: dict, created_by: str, description: Optional[str] = None) -> WorkflowDefinitionMeta:
        """Creates a new workflow definition as DRAFT."""
        async with self.session_factory() as db:
            # Check if name exists to increment version
            stmt = select(DbWorkflowDefinition).where(DbWorkflowDefinition.name == name).order_by(DbWorkflowDefinition.version.desc()).limit(1)
            result = await db.execute(stmt)
            latest = result.scalar_one_or_none()

            new_version = (latest.version + 1) if latest else 1

            db_def = DbWorkflowDefinition(
                name=name,
                version=new_version,
                description=description,
                status="DRAFT",
                definition_payload=definition_payload,
                created_by=created_by
            )
            db.add(db_def)
            await db.commit()
            await db.refresh(db_def)
            
            logger.info(f"Created Workflow Draft: {db_def.name} v{db_def.version}")
            return self._to_pydantic(db_def)

    async def publish_workflow(self, workflow_id: str) -> WorkflowDefinitionMeta:
        """Marks a workflow as PUBLISHED, allowing instances to be created from it."""
        async with self.session_factory() as db:
            stmt = select(DbWorkflowDefinition).where(DbWorkflowDefinition.id == workflow_id)
            result = await db.execute(stmt)
            db_def = result.scalar_one_or_none()
            
            if not db_def:
                raise ValueError(f"Workflow {workflow_id} not found.")
                
            db_def.status = "PUBLISHED"
            await db.commit()
            await db.refresh(db_def)
            
            logger.info(f"Published Workflow: {db_def.name} v{db_def.version}")
            return self._to_pydantic(db_def)

    async def get_published_version(self, name: str) -> Optional[WorkflowDefinitionMeta]:
        """Gets the highest version of a workflow that is published."""
        async with self.session_factory() as db:
            stmt = select(DbWorkflowDefinition).where(
                DbWorkflowDefinition.name == name,
                DbWorkflowDefinition.status == "PUBLISHED"
            ).order_by(DbWorkflowDefinition.version.desc()).limit(1)
            
            result = await db.execute(stmt)
            db_def = result.scalar_one_or_none()
            
            return self._to_pydantic(db_def) if db_def else None

    def _to_pydantic(self, db_obj: DbWorkflowDefinition) -> WorkflowDefinitionMeta:
        return WorkflowDefinitionMeta(
            id=db_obj.id,
            name=db_obj.name,
            version=db_obj.version,
            description=db_obj.description,
            status=db_obj.status,
            states=db_obj.definition_payload.get("states", []),
            transitions=db_obj.definition_payload.get("transitions", [])
        )
