# Assessment Engine & Competency Evaluation Architecture

## Overview
The Assessment Engine (Enterprise Implementation Plan 3.5) represents a robust, highly modular evaluation framework for industrial learning. Moving beyond standard multiple-choice quizzes, this engine evaluates theoretical understanding, safety awareness, equipment knowledge, and practical decision-making through dynamic questioning. The engine directly integrates with the Competency Evaluation Framework to map raw scores into professional readiness metrics.

## Assessment Structure
An `Assessment` acts as the container configuration.
- **Constraints**: Enforces time limits, maximum attempts, passing percentages, and randomize options.
- **Metadata**: Connects assessments to specific roles, departments, or learning modules.
- **Payload**: Contains an array of polymorphic `Question` objects.

## Question Bank Architecture
The `Question` model utilizes Pydantic discriminated unions. This means an assessment can seamlessly interleave standard questions with interactive hotspots and practical case studies.

### Supported Question Types
- **Standard**: `SINGLE_CHOICE`, `MULTIPLE_CHOICE`, `TRUE_FALSE`, `FILL_IN_BLANK`, `MATCHING`, `SEQUENCE`.
- **Advanced / Industrial**:
  - `IMAGE_HOTSPOT`: E.g., clicking the unsafe element on an equipment image.
  - `SCENARIO`: Evaluates multi-step decision making.
  - `CHECKLIST`: Practical step-by-step validations.
  - `PROCESS_FLOW`: Arranging manufacturing steps in order.
- **Future AI Types**: `AI_ORAL` (conversational evaluations) and `PRACTICAL` (rubric-based observations).

### Question Features
Every question supports deep context, including image/video references, PDF attachments, hints, detailed explanations, negative marking, and mappings to specific `CompetencyArea`s.

## Scoring Engine
The `AssessmentService` houses the Scoring Engine logic.
- **Attempt Tracking**: Secures session data from `NOT_STARTED` to `SUBMITTED`.
- **Evaluation**: Calculates automatic scores, applying partial marks (if configured) and deducting for negative marks.
- **Results**: Generates an `AssessmentResult` highlighting the overall score, identifying strengths/weaknesses (via competency mappings), and recommending retakes or specific lessons.

## Competency Evaluation Framework
The `CompetencyService` listens to the output of the Scoring Engine.
- **CompetencyProfile**: A user's living document tracking their `overall_readiness_score` and specific `area_scores`.
- **Evaluated Areas**: `MANUFACTURING_KNOWLEDGE`, `SAFETY_AWARENESS`, `QUALITY_UNDERSTANDING`, `EQUIPMENT_KNOWLEDGE`, `DEPARTMENT_READINESS`, `PROBLEM_SOLVING`, `DECISION_MAKING`.
- **Feedback Loop**: When an assessment is finalized, the scores from individual mapped questions flow into the user's `CompetencyProfile`, creating a targeted view of their industrial readiness.

## Future AI Integrations
- **AI Question Generator**: LLMs can autonomously generate questions (e.g., pulling from SOPs) and format them into the polymorphic schema.
- **Dynamic Difficulty Adjustment**: The Assessment configuration can be hooked into an AI agent to adjust question difficulty in real-time based on the user's live `CompetencyProfile`.
- **AI Oral & Practical Evaluation**: Expanding the engine beyond screen clicks into conversational assessments (analyzing audio transcripts against grading rubrics).
