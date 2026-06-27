# Enterprise Safety, Compliance & Emergency Response Platform Architecture

## Overview
The Safety & Compliance Architecture (Enterprise Implementation Plan 3.12) is the gatekeeper of the industrial learning platform. Before a user can engage with the `manufacturing` or `equipment` modules, they must be validated against the strict models defined in this platform.

## Architectural Segregation
To ensure scalability (particularly for future SAP HR synchronization), this platform is separated into three highly specialized backend modules:

### 1. Compliance Module (`compliance`)
The rules engine.
- **ComplianceRule**: Defines a mandatory organizational requirement (e.g., "All EAF Operators must complete Fire Safety Module every 365 days"). It tracks the `grace_period_days` and `validity_period_days`.
- **UserComplianceRecord**: A specific instance evaluating a user against a `ComplianceRule`. It handles state mapping to `ComplianceStatus` (COMPLIANT, NON_COMPLIANT, EXPIRED, GRACE_PERIOD).
- **Engine**: The `ComplianceFramework` acts as the strict judge. It does not store the learning content itself; it merely evaluates completion flags from the Safety module.

### 2. Safety Module (`safety`)
The foundational knowledge repository.
- **SafetyModule**: The actual wrapper for learning content. It has reserved `ai_safety_coach_prompt` hooks for future generative learning and `iot_sensor_triggers` for live plant monitoring.
- **Hazard**: A standardized dictionary of risks. Each hazard explicitly links to necessary `ControlMeasure`s and `PPEType`s to eliminate tribal knowledge.
- **PPEItem**: Detailed schemas mapping out the specific inspection checklists and replacement criteria for safety gear (Helmets, Respirators, etc.).

### 3. Emergency Response Module (`emergency`)
The critical procedural mapping.
- **EmergencyProcedure**: Distinct from standard SOPs. These models require an `escalation_chain` (who to call, in what order) and `immediate_actions`.
- **Future VR Integration**: A dedicated `vr_simulation_id` string has been architected into the model to map specific emergency responses (e.g., "Chemical Spill") directly into future interactive 3D simulations.

## Frontend Interaction
The frontend utilizes `SafetyDashboardService.ts` to query across all three modules simultaneously, presenting a unified `SafetyDashboardStats` payload to managers, providing a real-time compliance percentage for their department.
