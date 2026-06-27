import logging
from modules.knowledge_intake.models import IntakeJob, ProposedRelationship, ProposedEntity

logger = logging.getLogger("RelationshipDiscovery")

class RelationshipDiscoveryService:
    """
    Simulates an AI graph analyzer that finds connections between proposed entities
    and existing entities, including SAP placeholders.
    """
    
    def process(self, job: IntakeJob) -> IntakeJob:
        logger.info(f"Discovering relationships for: {job.filename}")
        
        if not job.proposed_entities:
            return job
            
        # The primary document entity
        primary_doc = job.proposed_entities[0]
        
        # 1. Link to other proposed entities
        for ent in job.proposed_entities[1:]:
            if ent.entity_type == "equipment":
                rel = ProposedRelationship(
                    source_id=primary_doc.id,
                    target_id=ent.id,
                    relationship_type="REFERENCES_EQUIPMENT"
                )
                job.proposed_relationships.append(rel)
                
        # 2. Create SAP Placeholders
        if "sap" in job.filename.lower() or primary_doc.entity_type in ["equipment"]:
            sap_placeholder = ProposedEntity(
                entity_type="sap_unresolved_mapping",
                display_name=f"SAP Sync: {primary_doc.display_name}",
                proposed_metadata={"sync_status": "PENDING"}
            )
            job.proposed_entities.append(sap_placeholder)
            job.sap_placeholders_created += 1
            
            job.proposed_relationships.append(ProposedRelationship(
                source_id=primary_doc.id,
                target_id=sap_placeholder.id,
                relationship_type="HAS_SAP_MAPPING"
            ))
            
        # 3. Simulate Hyperlink connections (e.g. associating to a default department)
        job.proposed_relationships.append(ProposedRelationship(
            source_id=primary_doc.id,
            target_id="dept-1", # Assume this exists from seeder
            relationship_type="BELONGS_TO_DEPARTMENT"
        ))
            
        logger.info(f"Discovered {len(job.proposed_relationships)} relationships.")
        return job
