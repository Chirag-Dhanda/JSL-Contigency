# Enterprise AI SOP Expert & Operational Guidance

## Overview
Implementation Plan 4.9 adds the SOP Expert agent to the Copilot. Unlike generic chatbot queries, asking about a Standard Operating Procedure involves physical safety risks. Therefore, the SOP Expert is architected with strict validation middleware to ensure compliance.

## 1. SOP AI Engine (`modules/sop_ai`)
The `SOPAIEngine` is the entry point for procedure questions.
- **`SectionNavigator`**: SOPs are often dozens of pages long. If a user asks "What are the quality checks?", the Navigator intercepts the query and maps it to the structural section "Quality Checks" in the Vector DB, preventing the AI from hallucinating checks from other parts of the document.
- **`KnowledgeLinker`**: Proactively fetches related data (like associated e-learning lessons or equipment IDs) and bundles them into the `SOPAIResponse`.
- **`SOPAIResponse` Schema**: Requires that the answer explicitly states the `Referenced SOP`, the exact `Referenced Section`, and, crucially, includes arrays for `mandatory_safety_notices` and `required_ppe`.

## 2. Safety Validation Middleware (`modules/procedure_assistant`)
- **`SafetyValidator`**: This is a non-negotiable step in the engine. *Before* the AI response is delivered to the frontend, the `SafetyValidator` scans the draft answer. If the AI is explaining how to operate high-voltage equipment but failed to mention the PPE required by that SOP, the Validator intercepts the payload, flags it as `is_safe = False`, and forcefully injects the mandatory PPE requirements and safety warnings into the final output.

## 3. Operational Guidance (`modules/operational_guidance`)
- **`SOPWalkthroughManager`**: Provides a stateful tracker (`current_step`, `total_steps`, `checkpoints_cleared`) stored in-memory per `user_id`. This allows an operator to ask the AI to "Go to the next step" without having to re-explain their context.
- **`OperationalModes`**: Enums (`LEARNING`, `OPERATIONAL`, `EXPERT`) that will act as a system prompt modifier to adjust the verbosity of the AI's explanation based on the user's current need.

## 4. Frontend Integration
The `SOPExpertUI.jsx` component was built to specifically catch the `SOPAIResponse` payload. It prominently renders the `SAFETY NOTICE` block in dark red, and the `REQUIRED PPE` block in teal above the actual procedure text, ensuring that operators cannot read the operational steps without first acknowledging the safety constraints injected by the middleware.
