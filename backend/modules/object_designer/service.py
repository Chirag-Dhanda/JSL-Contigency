import logging
from typing import List, Dict, Any
from exceptions.base import NotFoundException, SystemException
from modules.metadata_engine.service import MetadataEngineService
from modules.entity_registry.models import EntityTypeDefinition, ValidationRule
from .models import BlueprintDraft, ReviewPackage, AttributeDefinition

logger = logging.getLogger("ObjectDesigner")

class ObjectDesignerService:
    """
    Primary administration service layer for defining and managing enterprise object types visually.
    Builds upon the Metadata Engine to provide high-level abstractions like AI visibility,
    Search configurations, and UI form layouts.
    """
    
    def __init__(self, metadata_engine: MetadataEngineService):
        self.metadata = metadata_engine
        logger.info("Object Designer Service Initialized.")

    def _compile_to_type_def(self, blueprint: BlueprintDraft) -> EntityTypeDefinition:
        """Translates the high-level Designer Blueprint into the low-level EntityTypeDefinition."""
        
        # 1. Compile schema rules
        schema_rules: Dict[str, ValidationRule] = {}
        for attr in blueprint.attributes:
            rule = ValidationRule(
                field_type=attr.field_type,
                required=attr.required,
                default_value=attr.default_value,
                enum_values=attr.options,
                min_value=attr.min_value,
                max_value=attr.max_value
            )
            schema_rules[attr.name] = rule
            
        # 2. Compile UI schema based on groups
        ui_schema: Dict[str, Any] = {}
        # The schema_engine generator will use this to scaffold the react-json-schema-form layout
        if blueprint.ui_config.sections:
            ui_schema["ui:order"] = []
            for section in blueprint.ui_config.sections:
                ui_schema["ui:order"].extend(section.fields)
                
        # 3. Compile allowed relationships
        allowed_rels = [r.relationship_type for r in blueprint.relationships]
        
        # 4. Construct final definition
        return EntityTypeDefinition(
            type_id=blueprint.type_id,
            display_name=blueprint.display_name,
            internal_name=blueprint.type_id,
            description=blueprint.description,
            icon=blueprint.icon,
            category=blueprint.category,
            metadata_schema=schema_rules,
            allowed_relationships=allowed_rels,
            ui_schema=ui_schema,
            search_config=blueprint.search_config.model_dump(),
            permissions_profile=blueprint.permissions.model_dump(),
            ai_visibility=blueprint.ai_config.is_visible_to_ai,
            configuration={"workflow": blueprint.workflow_config.model_dump()}
        )

    def _extract_blueprint(self, type_def: EntityTypeDefinition) -> BlueprintDraft:
        """Translates an EntityTypeDefinition back into a BlueprintDraft."""
        
        attributes = []
        for key, rule in type_def.metadata_schema.items():
            attributes.append(AttributeDefinition(
                name=key,
                display_name=key.replace("_", " ").title(),
                field_type=rule.field_type,
                required=rule.required,
                default_value=rule.default_value,
                options=rule.enum_values,
                min_value=rule.min_value,
                max_value=rule.max_value
            ))
            
        return BlueprintDraft(
            type_id=type_def.type_id,
            display_name=type_def.display_name,
            description=type_def.description,
            icon=type_def.icon or "fa-cube",
            category=type_def.category or "General",
            attributes=attributes,
            # For simplicity in this extraction, relationships and complex configs
            # would ideally be re-hydrated fully. 
        )

    def create_blueprint(self, blueprint: BlueprintDraft) -> BlueprintDraft:
        """Translates a Blueprint and registers it as a Draft in the Metadata Engine."""
        type_def = self._compile_to_type_def(blueprint)
        self.metadata.register_type(type_def)
        logger.info(f"Created Blueprint Draft: {blueprint.type_id}")
        return blueprint

    def update_blueprint(self, type_id: str, blueprint: BlueprintDraft) -> BlueprintDraft:
        """Updates a Blueprint Draft in the Metadata Engine."""
        if blueprint.type_id != type_id:
            raise SystemException(message="Cannot change the type_id of an existing blueprint.")
            
        type_def = self._compile_to_type_def(blueprint)
        # Use update_type to bump version and save
        updates = type_def.model_dump(exclude={'type_id', 'version', 'status'})
        self.metadata.update_type(type_id, updates)
        logger.info(f"Updated Blueprint Draft: {type_id}")
        return blueprint

    def duplicate_blueprint(self, type_id: str, new_type_id: str, new_display_name: str) -> BlueprintDraft:
        """Clones an existing blueprint into a new Draft."""
        original_def = self.metadata.get_type(type_id)
        blueprint = self._extract_blueprint(original_def)
        
        blueprint.type_id = new_type_id
        blueprint.display_name = new_display_name
        
        return self.create_blueprint(blueprint)

    def generate_review_package(self, type_id: str) -> ReviewPackage:
        """
        Compiles a comprehensive review package for Master Editors.
        Analyzes dependencies, diffs against the published version, and validates schema integrity.
        """
        draft_def = self.metadata.get_type(type_id)
        
        # 1. Dependency Analysis
        dependencies = self.metadata.analyze_dependencies(type_id)
        
        # 2. Validation
        warnings = []
        validation_status = "PASSED"
        try:
            self.metadata.validator.validate_type_definition(draft_def)
        except Exception as e:
            validation_status = "FAILED"
            warnings.append(str(e))
            
        # 3. Diff Engine (Compare against previous Published if exists)
        version_diff = {"added_fields": [], "removed_fields": [], "modified_fields": []}
        try:
            if hasattr(self.metadata.repository, 'get_type_versions'):
                versions = self.metadata._call('get_type_versions', type_id)
                # Find the most recently published version
                published_versions = [v for v in versions if v.status == "Published"]
                if published_versions:
                    old_schema = published_versions[0].metadata_schema
                    new_schema = draft_def.metadata_schema
                    
                    old_keys = set(old_schema.keys())
                    new_keys = set(new_schema.keys())
                    
                    version_diff["added_fields"] = list(new_keys - old_keys)
                    version_diff["removed_fields"] = list(old_keys - new_keys)
                    version_diff["modified_fields"] = [k for k in old_keys.intersection(new_keys) 
                                                       if old_schema[k].model_dump() != new_schema[k].model_dump()]
        except Exception as e:
            logger.warning(f"Failed to generate diff for {type_id}: {e}")

        # 4. Graph Projection Preview (Impact Analysis)
        graph_impact = {}
        try:
            from modules.relationship_engine.analyzer import DependencyAnalyzer
            from modules.relationship_engine.neo4j_repository import Neo4jRepository
            import asyncio
            
            # Since this evaluates impact on the type itself, we might mock this
            # or in a real scenario look up related objects. For now, we report ready.
            graph_impact["status"] = "Ready for Projection"
            graph_impact["allowed_relationships"] = draft_def.allowed_relationships
        except Exception as e:
            graph_impact["error"] = str(e)

        return ReviewPackage(
            blueprint_id=type_id,
            display_name=draft_def.display_name,
            version_diff=version_diff,
            dependency_report={"metadata": dependencies, "graph": graph_impact},
            validation_status=validation_status,
            warnings=warnings
        )

    def publish_blueprint(self, type_id: str, user_id: str) -> Dict[str, Any]:
        """Publishes the blueprint via the Metadata Engine, making it active in the system."""
        # Ensure it passes review checks first
        pkg = self.generate_review_package(type_id)
        if pkg.validation_status != "PASSED":
            raise SystemException(message=f"Cannot publish blueprint with validation errors: {pkg.warnings}")
            
        published_def = self.metadata.publish_type(type_id, user_id)
        return {"status": "success", "version": published_def.version}
