import logging
import re
from typing import Dict, Any, List
from modules.entity_registry.models import EntityTypeDefinition, ValidationRule
from exceptions.base import SystemException

logger = logging.getLogger("SchemaValidator")

class SchemaValidator:
    """
    Validates dynamic entity metadata against the strict Schema Rules 
    defined in the Entity Registry.
    """
    
    def validate(self, metadata: Dict[str, Any], schema_def: EntityTypeDefinition) -> bool:
        """
        Validates the entire metadata payload against the schema definition.
        Raises SystemException if validation fails.
        """
        schema_rules = schema_def.metadata_schema
        
        # 1. Check Required Fields
        for key, rule in schema_rules.items():
            if rule.required and key not in metadata:
                # Use default value if missing and available
                if rule.default_value is not None:
                    metadata[key] = rule.default_value
                else:
                    raise SystemException(message=f"Validation Failed: Missing required field '{key}'")
                
        # 2. Check Custom Fields (If not allowed)
        if not schema_def.allow_custom_fields:
            for key in metadata.keys():
                if key not in schema_rules:
                    raise SystemException(message=f"Validation Failed: Custom field '{key}' is not permitted for type '{schema_def.type_id}'.")
                    
        # 3. Validate Individual Field Rules
        for key, value in metadata.items():
            if key in schema_rules:
                self._validate_field(key, value, schema_rules[key])
                
        return True

    def _validate_field(self, key: str, value: Any, rule: ValidationRule):
        """Validates a single field against its specific rule."""
        if value is None:
            if rule.required:
                raise SystemException(message=f"Validation Failed: Field '{key}' is required.")
            return

        # Type Check
        text_types = ["text", "long_text", "rich_text", "email", "phone", "url"]
        numeric_types = ["number", "decimal", "currency", "percentage", "duration"]
        
        if rule.field_type in text_types and not isinstance(value, str):
            raise SystemException(message=f"Validation Failed: Field '{key}' must be a string/text.")
        elif rule.field_type in numeric_types and not isinstance(value, (int, float)):
            raise SystemException(message=f"Validation Failed: Field '{key}' must be a number.")
        elif rule.field_type == "boolean" and not isinstance(value, bool):
            raise SystemException(message=f"Validation Failed: Field '{key}' must be a boolean.")
        elif rule.field_type in ["list", "multi_select"] and not isinstance(value, list):
            raise SystemException(message=f"Validation Failed: Field '{key}' must be a list.")
            
        # String Constraints
        if isinstance(value, str):
            if rule.min_length is not None and len(value) < rule.min_length:
                raise SystemException(message=f"Validation Failed: Field '{key}' must be at least {rule.min_length} characters.")
            if rule.max_length is not None and len(value) > rule.max_length:
                raise SystemException(message=f"Validation Failed: Field '{key}' must be at most {rule.max_length} characters.")
            if rule.regex is not None:
                if not re.match(rule.regex, value):
                    raise SystemException(message=f"Validation Failed: Field '{key}' does not match required format.")
                
        # Numeric Constraints
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if rule.min_value is not None and value < rule.min_value:
                raise SystemException(message=f"Validation Failed: Field '{key}' must be >= {rule.min_value}.")
            if rule.max_value is not None and value > rule.max_value:
                raise SystemException(message=f"Validation Failed: Field '{key}' must be <= {rule.max_value}.")
                
        # Enum / Dropdown Constraints
        if rule.enum_values is not None and rule.field_type in ["dropdown", "text"]:
            if value not in rule.enum_values:
                raise SystemException(message=f"Validation Failed: Field '{key}' must be one of {rule.enum_values}.")
        
        if rule.enum_values is not None and rule.field_type == "multi_select":
            if not all(item in rule.enum_values for item in value):
                raise SystemException(message=f"Validation Failed: All items in '{key}' must be from {rule.enum_values}.")
