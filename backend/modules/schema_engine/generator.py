import logging
from typing import Dict, Any
from modules.entity_registry.models import EntityTypeDefinition

logger = logging.getLogger("SchemaGenerator")

class SchemaGenerator:
    """
    Dynamically generates standard schemas (JSON Schema, UI Schema) 
    from EKOS EntityTypeDefinitions.
    """
    
    def generate_json_schema(self, type_def: EntityTypeDefinition) -> Dict[str, Any]:
        """
        Converts the custom metadata_schema into a standard JSON Schema (Draft 7+).
        Useful for external API validation or dynamic forms.
        """
        schema: Dict[str, Any] = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": type_def.display_name,
            "description": type_def.description or f"Schema for {type_def.display_name}",
            "properties": {},
            "required": []
        }
        
        for key, rule in type_def.metadata_schema.items():
            prop: Dict[str, Any] = {}
            
            # Map field_type to JSON Schema type
            if rule.field_type in ["text", "long_text", "rich_text", "email", "phone", "url", "dropdown"]:
                prop["type"] = "string"
                if rule.min_length is not None:
                    prop["minLength"] = rule.min_length
                if rule.max_length is not None:
                    prop["maxLength"] = rule.max_length
                if rule.regex:
                    prop["pattern"] = rule.regex
                    
            elif rule.field_type in ["number", "decimal", "currency", "percentage", "duration"]:
                prop["type"] = "number"
                if rule.min_value is not None:
                    prop["minimum"] = rule.min_value
                if rule.max_value is not None:
                    prop["maximum"] = rule.max_value
                    
            elif rule.field_type == "boolean":
                prop["type"] = "boolean"
                
            elif rule.field_type in ["list", "multi_select"]:
                prop["type"] = "array"
                prop["items"] = {"type": "string"}
                
            # Enum constraints
            if rule.enum_values:
                if rule.field_type in ["dropdown", "text"]:
                    prop["enum"] = rule.enum_values
                elif rule.field_type == "multi_select":
                    prop["items"]["enum"] = rule.enum_values
                    
            if rule.default_value is not None:
                prop["default"] = rule.default_value
                
            schema["properties"][key] = prop
            
            if rule.required:
                schema["required"].append(key)
                
        if not schema["required"]:
            del schema["required"]
            
        if not type_def.allow_custom_fields:
            schema["additionalProperties"] = False
            
        return schema
        
    def generate_ui_schema(self, type_def: EntityTypeDefinition) -> Dict[str, Any]:
        """
        Merges the user-provided ui_schema with default UI heuristics.
        """
        ui_schema = type_def.ui_schema.copy()
        
        for key, rule in type_def.metadata_schema.items():
            if key not in ui_schema:
                ui_schema[key] = {}
                
            if rule.field_type == "long_text":
                ui_schema[key].setdefault("ui:widget", "textarea")
            elif rule.field_type == "boolean":
                ui_schema[key].setdefault("ui:widget", "checkbox")
            elif rule.field_type == "date":
                ui_schema[key].setdefault("ui:widget", "date")
            elif rule.field_type == "datetime":
                ui_schema[key].setdefault("ui:widget", "datetime")
                
            if rule.visibility_rule:
                ui_schema[key]["ui:hidden"] = rule.visibility_rule
                
        return ui_schema
