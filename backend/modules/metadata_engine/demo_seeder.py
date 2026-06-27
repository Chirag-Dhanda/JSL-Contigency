import logging
from modules.metadata_engine.service import MetadataEngineService
from modules.entity_registry.models import EntityTypeDefinition, ValidationRule

logger = logging.getLogger("DemoSeeder")

def seed_enterprise_metadata(engine: MetadataEngineService):
    logger.info("Seeding Enterprise Demo Metadata...")

    # ---------------------------------------------------------
    # 1. REGISTER TEMPLATES (TYPES)
    # ---------------------------------------------------------
    
    # Machine Template
    engine.register_type(EntityTypeDefinition(
        type_id="machine",
        display_name="Manufacturing Equipment",
        description="A piece of industrial machinery",
        icon="fa-industry",
        category="Manufacturing",
        metadata_schema={
            "manufacturer": ValidationRule(field_type="text", required=True),
            "plant": ValidationRule(field_type="dropdown", enum_values=["Jajpur", "Hisar", "Pathredi"], required=True),
            "commission_date": ValidationRule(field_type="date", required=True),
            "plc_link": ValidationRule(field_type="url", required=False),
            "scada_link": ValidationRule(field_type="url", required=False),
            "status": ValidationRule(field_type="dropdown", enum_values=["Active", "Maintenance", "Decommissioned"], default_value="Active")
        }
    ))

    # Department Template
    engine.register_type(EntityTypeDefinition(
        type_id="department",
        display_name="Enterprise Department",
        description="An organizational unit",
        icon="fa-sitemap",
        category="Organization",
        metadata_schema={
            "head": ValidationRule(field_type="text", required=True),
            "budget": ValidationRule(field_type="currency", required=False),
            "cost_center": ValidationRule(field_type="text", required=True, regex=r"^CC-\d{4}$"),
            "sap_module": ValidationRule(field_type="sap_placeholder", required=False)
        }
    ))

    # Knowledge Document Template
    engine.register_type(EntityTypeDefinition(
        type_id="knowledge_doc",
        display_name="Knowledge Document",
        description="SOPs, Policies, Work Instructions",
        icon="fa-file-alt",
        category="Knowledge",
        metadata_schema={
            "doc_type": ValidationRule(field_type="dropdown", enum_values=["SOP", "Policy", "Work Instruction", "Checklist", "Assessment"], required=True),
            "content": ValidationRule(field_type="rich_text", required=True),
            "review_date": ValidationRule(field_type="date", required=True),
            "ai_summary": ValidationRule(field_type="ai_generated", required=False)
        }
    ))

    # ---------------------------------------------------------
    # 2. POPULATE DEMO OBJECTS
    # ---------------------------------------------------------

    # Manufacturing Entities
    machines = [
        {"name": "EAF-01", "display": "Electric Arc Furnace 1", "plant": "Jajpur", "date": "2015-05-01"},
        {"name": "LRF-02", "display": "Ladle Refining Furnace 2", "plant": "Jajpur", "date": "2016-08-15"},
        {"name": "AOD-01", "display": "Argon Oxygen Decarburization", "plant": "Hisar", "date": "2012-11-20"},
        {"name": "CCM-03", "display": "Continuous Casting Machine", "plant": "Jajpur", "date": "2018-02-10"},
        {"name": "HRM-01", "display": "Hot Rolling Mill", "plant": "Jajpur", "date": "2015-06-01"},
        {"name": "CRM-02", "display": "Cold Rolling Mill", "plant": "Hisar", "date": "2014-04-12"},
        {"name": "PL-01", "display": "Pickling Line", "plant": "Pathredi", "date": "2019-09-01"},
        {"name": "AL-01", "display": "Annealing Line", "plant": "Pathredi", "date": "2019-10-01"}
    ]

    for m in machines:
        engine.create_object(
            name=m["name"],
            entity_type="machine",
            display_name=m["display"],
            created_by="system_seeder",
            metadata={
                "manufacturer": "SMS Group",
                "plant": m["plant"],
                "commission_date": m["date"],
                "status": "Active"
            }
        )

    # Department Entities
    departments = [
        {"name": "dept-production", "display": "Production", "head": "Rajesh Kumar", "cc": "CC-1001", "sap": "PP"},
        {"name": "dept-meltshop", "display": "Melt Shop", "head": "Amit Sharma", "cc": "CC-1002", "sap": "PP"},
        {"name": "dept-qa", "display": "Quality Assurance", "head": "Sneha Gupta", "cc": "CC-2001", "sap": "QM"},
        {"name": "dept-mech", "display": "Mechanical Maintenance", "head": "Vikram Singh", "cc": "CC-3001", "sap": "PM"},
        {"name": "dept-hr", "display": "Human Resources", "head": "Priya Patel", "cc": "CC-4001", "sap": "HCM"}
    ]

    for d in departments:
        engine.create_object(
            name=d["name"],
            entity_type="department",
            display_name=d["display"],
            created_by="system_seeder",
            metadata={
                "head": d["head"],
                "cost_center": d["cc"],
                "sap_module": d["sap"]
            }
        )
        
    # Knowledge Entities
    docs = [
        {"name": "sop-eaf-start", "display": "EAF Startup Procedure", "type": "SOP", "date": "2026-12-31"},
        {"name": "pol-safety", "display": "Plant Safety Policy", "type": "Policy", "date": "2027-01-01"},
        {"name": "chk-crane", "display": "Overhead Crane Daily Checklist", "type": "Checklist", "date": "2026-10-15"}
    ]

    for doc in docs:
        engine.create_object(
            name=doc["name"],
            entity_type="knowledge_doc",
            display_name=doc["display"],
            created_by="system_seeder",
            metadata={
                "doc_type": doc["type"],
                "content": "<p>Standardized content generated by system.</p>",
                "review_date": doc["date"]
            }
        )

    logger.info("Demo Metadata Seeding Complete.")
