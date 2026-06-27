# Learning Intelligence & Analytics Engine Architecture

## Overview
The Learning Intelligence Engine (Enterprise Implementation Plan 3.6) is the culmination of tracking user progress across learning modules and assessing competency growth. This architecture aggregates data into scalable visualization formats, providing distinct intelligence for employees, managers, and organizational admins. 

## Progress Engine
The `progress` module serves as the highly granular tracker for user activities.

### Progress Record
- **Scope**: Tracks progress at an atomic entity level (e.g., Lesson, Roadmap, Assessment, Station).
- **Core Metrics**: Standardizes tracking through `completion_percentage`, `time_spent_mins`, and `average_session_mins`.
- **Status Lifecycle**: State machine moving from `NOT_STARTED` -> `IN_PROGRESS` -> `COMPLETED`.

## Analytics Engine
The `analytics` module acts as an aggregator. It consumes data from the `ProgressEngine` and the `CompetencyService` to construct visualization-ready payloads. By standardizing visualization schemas on the backend (e.g., `TrendGraph`, `RadarChart`, `HeatMap`), frontend applications or future SAP integrations can simply render the data generically.

### Dashboard Types
1. **Employee Analytics**: Focuses on individual metrics. Highlighting recent activity (trend lines), competency footprints (radar charts), and actionable pending training.
2. **Manager Dashboard**: Focuses on team health. Highlights team completion percentages, identifies weak competencies globally, and lists employees needing assistance.
3. **Admin Dashboard**: Focuses on organizational trends. Provides cross-department heat maps, learning growth trends, and overall training coverage.

## Recommendation Engine
While initially a mock, the Recommendation Architecture utilizes the `Recommendation` model. 
- Analyzes weak areas in a user's `CompetencyProfile`.
- Recommends specific `target_entity_id`s (like Lessons or Roadmaps) with a generated AI `confidence_score`.

## Reporting Architecture
Standardized models (`IndividualReport`, `DepartmentReport`) consolidate the dashboard metrics into snapshot payloads, ideal for future PDF exports or SAP HR synchronization.

## Future AI Integrations
- **AI Analytics**: AI can run regressions across `ProgressRecord` `time_spent_mins` vs `AssessmentResult` `overall_score_percent` to detect ineffective lesson materials autonomously.
- **AI Recommendation Model**: The Recommendation engine can be upgraded to generate live personalized paths instead of just linking single entities.
