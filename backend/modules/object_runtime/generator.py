import logging
from typing import Dict, Any
from modules.object_definitions.templates import VisualObjectDefinition
from modules.entity_registry.models import EntityTypeDefinition, ValidationRule
from modules.entity_registry.service import EntityRegistryService

logger = logging.getLogger("RuntimeGenerator")

class RuntimeGeneratorService:
    """
    Compiles a high-level visual 'ObjectDefinition' into a low-level 
    'EntityTypeDefinition' that the core Metadata Engine understands.
    """
    
    def __init__(self, registry: EntityRegistryService):
        self.registry = registry
        logger.info("Runtime Generator Initialized.")
        
    def compile_and_register(self, visual_obj: VisualObjectDefinition) -> EntityTypeDefinition:
        """
        Translates visual fields into strict ValidationRules and registers the type.
        """
        logger.info(f"Compiling visual object: {visual_obj.type_id}")
        
        schema_dict: Dict[str, ValidationRule] = {}
        default_dict: Dict[str, Any] = {}
        
        # 1. Translate Fields
        for field in visual_obj.fields:
            # Map visual field types to underlying validation engine types
            core_type = self._map_field_type(field.field_type)
            
            rule = ValidationRule(
                field_type=core_type,
                required=field.validation.required,
                min_length=field.validation.min_length,
                max_length=field.validation.max_length,
                min_value=field.validation.min_value,
                max_value=field.validation.max_value,
                enum_values=field.validation.allowed_values
            )
            schema_dict[field.field_id] = rule
            
            if field.default_value is not None:
                default_dict[field.field_id] = field.default_value
                
        # 2. Build the Core Definition
        core_def = EntityTypeDefinition(
            type_id=visual_obj.type_id,
            display_name=visual_obj.display_name,
            description=visual_obj.description,
            metadata_schema=schema_dict,
            default_metadata=default_dict,
            is_active=True,
            # If the designer explicitly defined fields, we might disable custom fields
            # to enforce strictness, but for Stage 5.4 we keep it flexible.
            allow_custom_fields=True 
        )
        
        # 3. Register it
        registered_type = self.registry.register_type(core_def)
        logger.info(f"Successfully compiled and registered {visual_obj.type_id} into the Entity Registry.")
        
        return registered_type
        
    def _map_field_type(self, visual_type: str) -> str:
        """Maps UI concepts to core engine concepts."""
        type_mapping = {
            "TEXT": "string",
            "LONG_TEXT": "string",
            "NUMBER": "number",
            "BOOLEAN": "boolean",
            "DROPDOWN": "string",
            "MULTI_SELECT": "list",
            "DATE": "string",
            "ENTITY_REF": "string",
            "FILE": "string"
        }
        return type_mapping.get(visual_type, "string")
