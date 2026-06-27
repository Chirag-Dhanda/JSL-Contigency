from enum import Enum

class KnowledgeCollection(str, Enum):
    MANUFACTURING = "manufacturing"
    SAFETY = "safety"
    SOP = "sop"
    EQUIPMENT = "equipment"
    LEARNING_MODULES = "learning_modules"
    ASSESSMENTS = "assessments"
    POLICIES = "policies"
    DEPARTMENT_RESOURCES = "department_resources"
    QUALITY = "quality"
    MAINTENANCE = "maintenance"
    SAP_KNOWLEDGE = "sap_knowledge"
    PLC_KNOWLEDGE = "plc_knowledge"
    SCADA_KNOWLEDGE = "scada_knowledge"
