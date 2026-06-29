from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from modules.entity_registry.models import EntityTypeDefinition

class AttributeDefinition(BaseModel):
    """EOD high-level abstraction for a field."""
    name: str
    display_name: str
    field_type: str = Field(..., description="text, number, boolean, date, enum, multiselect, reference, etc.")
    required: bool = False
    default_value: Optional[Any] = None
    options: Optional[List[str]] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    is_searchable: bool = True
    is_pii: bool = False

class RelationshipDefinition(BaseModel):
    """EOD high-level abstraction for graph links."""
    target_type_id: str
    relationship_type: str = Field(default="related_to")
    direction: str = Field(default="DIRECTED")

class UISection(BaseModel):
    title: str
    fields: List[str]
    collapsible: bool = False

class UISchemaConfig(BaseModel):
    sections: List[UISection] = Field(default_factory=list)

class SearchConfiguration(BaseModel):
    searchable_fields: List[str] = Field(default_factory=list)
    filterable_fields: List[str] = Field(default_factory=list)
    semantic_weight: int = 1

class WorkflowConfiguration(BaseModel):
    requires_approval: bool = False
    approval_groups: List[str] = Field(default_factory=list)

class AIConfiguration(BaseModel):
    is_visible_to_ai: bool = True
    is_embeddable: bool = True
    classification_level: str = "Internal"

class PermissionConfiguration(BaseModel):
    view_roles: List[str] = Field(default_factory=lambda: ["*"])
    edit_roles: List[str] = Field(default_factory=lambda: ["CONTENT_EDITOR", "MASTER_EDITOR", "PLATFORM_ADMIN"])

class BlueprintDraft(BaseModel):
    """The master configuration payload handled by the Object Designer UI."""
    type_id: str
    display_name: str
    description: Optional[str] = None
    icon: str = "fa-cube"
    category: str = "General"
    attributes: List[AttributeDefinition] = Field(default_factory=list)
    relationships: List[RelationshipDefinition] = Field(default_factory=list)
    ui_config: UISchemaConfig = Field(default_factory=UISchemaConfig)
    search_config: SearchConfiguration = Field(default_factory=SearchConfiguration)
    workflow_config: WorkflowConfiguration = Field(default_factory=WorkflowConfiguration)
    ai_config: AIConfiguration = Field(default_factory=AIConfiguration)
    permissions: PermissionConfiguration = Field(default_factory=PermissionConfiguration)

class ReviewPackage(BaseModel):
    """Summary generated before publication for Master Editor review."""
    blueprint_id: str
    display_name: str
    version_diff: Dict[str, Any]
    dependency_report: Dict[str, Any]
    validation_status: str = "PASSED"
    warnings: List[str] = Field(default_factory=list)
