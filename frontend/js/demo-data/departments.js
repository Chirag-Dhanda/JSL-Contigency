// ========================================
// demo-data/departments.js - Enterprise Manufacturing Departments
// ========================================

export const departmentData = {
    "Production": {
        icon: "fa-industry",
        desc: "Overall steelmaking production control, scheduling and SAP PP module integration.",
        head: "Rajesh Kumar",
        plant: "Jajpur"
    },
    "Melt Shop": {
        icon: "fa-fire",
        desc: "Electric Arc Furnace, Ladle Refining Furnace and Argon Oxygen Decarburization operations.",
        head: "Amit Sharma",
        plant: "Jajpur"
    },
    "Rolling Mill": {
        icon: "fa-cog",
        desc: "Hot Rolling Mill, Cold Rolling Mill and downstream processing of flat steel products.",
        head: "Suresh Nair",
        plant: "Jajpur"
    },
    "Quality Assurance": {
        icon: "fa-microscope",
        desc: "Steel product inspection, lab testing, non-conformance management and SAP QM.",
        head: "Sneha Gupta",
        plant: "Hisar"
    },
    "Mechanical Maintenance": {
        icon: "fa-wrench",
        desc: "Preventive and corrective maintenance of all rotating and static equipment across the plant.",
        head: "Sanjay Yadav",
        plant: "Jajpur"
    },
    "Electrical Maintenance": {
        icon: "fa-bolt",
        desc: "HT/LT switchgear, transformer maintenance, drives and substation operations.",
        head: "Harish Reddy",
        plant: "Jajpur"
    },
    "Automation": {
        icon: "fa-microchip",
        desc: "PLC, SCADA, DCS, HMI programming and industrial digital infrastructure management.",
        head: "Vikram Singh",
        plant: "Jajpur"
    },
    "SAP Team": {
        icon: "fa-server",
        desc: "SAP PP, QM, PM, MM, HCM module implementation, support and SAP Basis operations.",
        head: "Arjun Pillai",
        plant: "Jajpur"
    },
    "Human Resources": {
        icon: "fa-users",
        desc: "Talent acquisition, training & development, payroll, compliance and SAP HCM.",
        head: "Priya Patel",
        plant: "Jajpur"
    },
    "Procurement": {
        icon: "fa-boxes-stacked",
        desc: "Raw material procurement, vendor management, SAP MM and contract administration.",
        head: "Vinod Bansal",
        plant: "Jajpur"
    },
    "Safety": {
        icon: "fa-shield-halved",
        desc: "Plant safety audits, hazard identification, PTW system and emergency response planning.",
        head: "Kiran Mishra",
        plant: "Jajpur"
    },
    "Logistics": {
        icon: "fa-truck",
        desc: "Raw material handling, finished goods dispatch, weigh-bridge operations and SAP LE.",
        head: "Ramesh Choudhary",
        plant: "Pathredi"
    }
};

export const equipmentData = [
    { name: "EAF-01", display: "Electric Arc Furnace", dept: "Melt Shop", status: "Active", plant: "Jajpur" },
    { name: "LRF-01", display: "Ladle Refining Furnace", dept: "Melt Shop", status: "Active", plant: "Jajpur" },
    { name: "AOD-01", display: "Argon Oxygen Decarburization", dept: "Melt Shop", status: "Active", plant: "Hisar" },
    { name: "CCM-01", display: "Continuous Casting Machine", dept: "Production", status: "Active", plant: "Jajpur" },
    { name: "HRM-01", display: "Hot Rolling Mill", dept: "Rolling Mill", status: "Active", plant: "Jajpur" },
    { name: "CRM-01", display: "Cold Rolling Mill", dept: "Rolling Mill", status: "Maintenance", plant: "Hisar" },
    { name: "PL-01", display: "Pickling Line", dept: "Rolling Mill", status: "Active", plant: "Pathredi" },
    { name: "AL-01", display: "Annealing Line", dept: "Rolling Mill", status: "Active", plant: "Pathredi" },
    { name: "SPM-01", display: "Skin Pass Mill", dept: "Rolling Mill", status: "Active", plant: "Jajpur" },
    { name: "SL-01", display: "Slitting Line", dept: "Production", status: "Active", plant: "Hisar" },
    { name: "GL-01", display: "Grinding Line", dept: "Mechanical Maintenance", status: "Active", plant: "Jajpur" },
    { name: "BAL-01", display: "Bright Annealing Line", dept: "Rolling Mill", status: "Active", plant: "Hisar" }
];

export const knowledgeDocs = [
    { name: "SOP-EAF-001", display: "EAF Startup & Shutdown Procedure", type: "SOP", dept: "Melt Shop" },
    { name: "SOP-LRF-002", display: "Ladle Refining Furnace Operating SOP", type: "SOP", dept: "Melt Shop" },
    { name: "SOP-HRM-003", display: "Hot Rolling Mill Roll Change Procedure", type: "SOP", dept: "Rolling Mill" },
    { name: "SOP-CCM-004", display: "Continuous Caster Tundish Preparation", type: "SOP", dept: "Production" },
    { name: "POL-SAF-001", display: "Plant Safety & PPE Policy", type: "Policy", dept: "Safety" },
    { name: "CHK-CRANE-001", display: "Overhead Crane Daily Inspection Checklist", type: "Checklist", dept: "Mechanical Maintenance" },
    { name: "CHK-HV-001", display: "High Voltage Switchgear Checklist", type: "Checklist", dept: "Electrical Maintenance" },
    { name: "TRN-SAP-PP-001", display: "SAP PP Module Training – Production Planning", type: "Training Module", dept: "SAP Team" }
];
