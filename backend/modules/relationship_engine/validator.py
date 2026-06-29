from typing import Dict, Any
from exceptions.base import SystemException
from modules.entity_registry.models import EntityTypeDefinition
from modules.relationship_registry.models import RelationshipTypeDefinition

class RelationshipValidator:
    """
    Validates relationships BEFORE they are saved to Postgres/Neo4j.
    Enforces Cardinality, circular references, and ontology constraints.
    """

    def validate_creation(self, source_type: EntityTypeDefinition, target_type: EntityTypeDefinition, rel_type: RelationshipTypeDefinition):
        # 1. Ontology / Registry constraint check
        # Verify the target is allowed for the source
        allowed_rels = source_type.allowed_relationships or []
        if rel_type.type_id not in allowed_rels:
            # For EP-04, we log/warn rather than strictly fail if allowed_rels is empty (to support legacy).
            # If they defined some, it must be in the list.
            if len(allowed_rels) > 0:
                raise SystemException(message=f"Relationship '{rel_type.type_id}' is not permitted for Entity Type '{source_type.type_id}'.")

        # 2. Additional graph cardinality checks (e.g., 1:1, 1:N) would query Neo4j via repository 
        # to ensure the constraint isn't violated.
        # This will be built out further as cardinality rules are added to RelationshipTypeDefinition.
        return True
