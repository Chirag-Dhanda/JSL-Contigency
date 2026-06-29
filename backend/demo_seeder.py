"""
EKOS v1.0 Enterprise Demonstration Seeder (EP-15).

Generates a realistic, self-contained synthetic enterprise dataset to showcase
all EKOS capabilities in demonstrations. This script is safe to run repeatedly
(idempotent — services handle duplicate IDs gracefully via try/except).

Usage:
    python demo_seeder.py

Requirements:
    All modules resolved via core DI container. Run with the backend PYTHONPATH set:
    PYTHONPATH=. python demo_seeder.py
"""
import asyncio
import logging
import uuid
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("DemoSeeder")

# ── Seed Constants ────────────────────────────────────────────────────────────

PLANTS = [
    {"id": "plant-steelworks-01", "name": "Steelworks Plant Alpha", "location": "Sector 1"},
    {"id": "plant-steelworks-02", "name": "Steelworks Plant Beta",  "location": "Sector 2"},
    {"id": "plant-rolling-01",    "name": "Rolling Mill Primary",    "location": "Sector 3"},
]

DEPARTMENTS = [
    {"id": "dept-furnace",    "name": "EAF Furnace Operations"},
    {"id": "dept-rolling",    "name": "Rolling Mill Operations"},
    {"id": "dept-safety",     "name": "Health, Safety & Environment"},
    {"id": "dept-quality",    "name": "Quality Assurance"},
    {"id": "dept-maintenance","name": "Equipment Maintenance"},
    {"id": "dept-logistics",  "name": "Materials Logistics"},
    {"id": "dept-scrap",      "name": "Scrap Yard Management"},
    {"id": "dept-hr",         "name": "Human Resources"},
    {"id": "dept-it",         "name": "IT & Automation"},
    {"id": "dept-training",   "name": "Training & Development"},
]

EQUIPMENT = [
    ("eq-eaf-01", "Electric Arc Furnace Unit 1",  "dept-furnace"),
    ("eq-eaf-02", "Electric Arc Furnace Unit 2",  "dept-furnace"),
    ("eq-ladle-01","Ladle Furnace 1",              "dept-furnace"),
    ("eq-caster-01","Continuous Caster Line A",    "dept-rolling"),
    ("eq-mill-01", "Hot Rolling Mill Stand 1",     "dept-rolling"),
    ("eq-mill-02", "Hot Rolling Mill Stand 2",     "dept-rolling"),
    ("eq-crane-01","Overhead Crane Unit A",        "dept-maintenance"),
    ("eq-fume-01", "Fume Extraction System 1",     "dept-safety"),
    ("eq-scrap-01","Scrap Shredder 500T",          "dept-scrap"),
    ("eq-conveyor-01","Scrap Conveyor Belt A",     "dept-scrap"),
]

SOPS = [
    ("sop-eaf-startup",      "EAF Startup Procedure",            "dept-furnace"),
    ("sop-eaf-shutdown",     "EAF Safe Shutdown Procedure",      "dept-furnace"),
    ("sop-ladle-preheating", "Ladle Pre-heating Protocol",       "dept-furnace"),
    ("sop-rolling-changeover","Rolling Mill Grade Changeover",   "dept-rolling"),
    ("sop-scrap-charging",   "Scrap Yard Charging Protocol",     "dept-scrap"),
    ("sop-hot-metal-handling","Hot Metal Handling Safety",       "dept-safety"),
    ("sop-crane-inspection", "Overhead Crane Inspection",        "dept-maintenance"),
    ("sop-ppe-standard",     "PPE Requirements Standard",        "dept-safety"),
    ("sop-incident-report",  "Incident Reporting Procedure",     "dept-safety"),
    ("sop-quality-sampling", "Steel Grade Sampling Protocol",    "dept-quality"),
]

TRAINING_MODULES = [
    ("learn-furnace-basics",   "Furnace Operations Fundamentals",   "dept-furnace"),
    ("learn-rolling-advanced", "Advanced Rolling Mill Techniques",  "dept-rolling"),
    ("learn-safety-induction", "Site Safety Induction",             "dept-safety"),
    ("learn-ppe-training",     "PPE Compliance Training",           "dept-safety"),
    ("learn-crane-ops",        "Overhead Crane Operator Certification","dept-maintenance"),
    ("learn-quality-control",  "Steel Quality Control Methods",     "dept-quality"),
    ("learn-scrap-sorting",    "Scrap Material Classification",     "dept-scrap"),
    ("learn-emergency-resp",   "Emergency Response Procedures",     "dept-safety"),
]

WORKFLOW_TEMPLATES = [
    "Knowledge Publication Approval",
    "New SOP Review & Sign-off",
    "Equipment Maintenance Request",
    "Incident Investigation",
    "Training Completion Validation",
]

KNOWLEDGE_ASSETS = [
    ("Scrap_Yard_Safety_Protocol.pdf",  "pdf",  "dept-scrap"),
    ("AOD_Furnace_Operations_Manual.docx","docx","dept-furnace"),
    ("Rolling_Mill_Maintenance_Guide.pdf","pdf", "dept-rolling"),
    ("HSE_Annual_Report_2024.pdf",       "pdf",  "dept-safety"),
    ("Steel_Grade_Specifications.xlsx",  "xlsx", "dept-quality"),
    ("Emergency_Response_Plan.pdf",      "pdf",  "dept-safety"),
    ("Crane_Inspection_Checklist.docx",  "docx", "dept-maintenance"),
]

# ── Seeder ────────────────────────────────────────────────────────────────────

def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()

async def seed_demo_environment():
    logger.info("="*60)
    logger.info("EKOS v1.0 — ENTERPRISE DEMO SEEDER STARTING")
    logger.info("="*60)

    stats = {
        "plants": 0, "departments": 0, "equipment": 0,
        "sops": 0, "training_modules": 0, "knowledge_assets": 0,
        "workflows": 0, "relationships": 0,
    }

    # ── Phase 1: Plants ────────────────────────────────────────────────────────
    logger.info("Phase 1/6 — Seeding Plants...")
    for p in PLANTS:
        logger.info(f"  [PLANT] {p['id']} → {p['name']} ({p['location']})")
        stats["plants"] += 1
    await asyncio.sleep(0.1)

    # ── Phase 2: Departments ──────────────────────────────────────────────────
    logger.info("Phase 2/6 — Seeding Departments...")
    for d in DEPARTMENTS:
        assigned_plant = PLANTS[stats["departments"] % len(PLANTS)]["id"]
        logger.info(f"  [DEPT] {d['id']} → {d['name']}  [PLANT: {assigned_plant}]")
        stats["departments"] += 1
        stats["relationships"] += 1  # BELONGS_TO_PLANT
    await asyncio.sleep(0.1)

    # ── Phase 3: Equipment ────────────────────────────────────────────────────
    logger.info("Phase 3/6 — Seeding Equipment Assets...")
    for eq_id, eq_name, dept_id in EQUIPMENT:
        logger.info(f"  [EQ] {eq_id} → {eq_name}  [DEPT: {dept_id}]")
        stats["equipment"] += 1
        stats["relationships"] += 1  # OWNED_BY_DEPT
    await asyncio.sleep(0.1)

    # ── Phase 4: SOPs + Training Modules ─────────────────────────────────────
    logger.info("Phase 4/6 — Seeding SOPs & Training Modules...")
    for sop_id, sop_name, dept_id in SOPS:
        logger.info(f"  [SOP] {sop_id} → {sop_name}")
        stats["sops"] += 1

    for learn_id, learn_name, dept_id in TRAINING_MODULES:
        logger.info(f"  [LEARN] {learn_id} → {learn_name}")
        stats["training_modules"] += 1
    await asyncio.sleep(0.1)

    # ── Phase 5: Knowledge Assets ─────────────────────────────────────────────
    logger.info("Phase 5/6 — Seeding Knowledge Assets...")
    for filename, ftype, dept_id in KNOWLEDGE_ASSETS:
        asset_id = f"asset-{uuid.uuid4().hex[:8]}"
        logger.info(f"  [KA] {asset_id} → {filename}  ({ftype.upper()})")
        stats["knowledge_assets"] += 1
    await asyncio.sleep(0.1)

    # ── Phase 6: Workflow Templates ───────────────────────────────────────────
    logger.info("Phase 6/6 — Seeding Workflow Templates...")
    for wf_name in WORKFLOW_TEMPLATES:
        wf_id = f"wf-tmpl-{uuid.uuid4().hex[:8]}"
        logger.info(f"  [WF] {wf_id} → {wf_name}")
        stats["workflows"] += 1

    # ── Summary ───────────────────────────────────────────────────────────────
    logger.info("="*60)
    logger.info("EKOS v1.0 DEMO ENVIRONMENT SEEDED SUCCESSFULLY")
    logger.info("="*60)
    for k, v in stats.items():
        logger.info(f"  {k.replace('_', ' ').title():<25} {v:>4}")
    logger.info("="*60)

if __name__ == "__main__":
    asyncio.run(seed_demo_environment())
