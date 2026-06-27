# Enterprise AI Personal Learning Mentor & Adaptive Intelligence

## Overview
Implementation Plan 4.10 establishes a dynamic, stateful AI Learning Mentor. This agent actively monitors a user's progress through the platform and adaptively modifies their curriculum to ensure compliance, safety, and competency development. 

**Strict Limitation**: The analysis frameworks here are rigidly bound to *Learning Competency*. They do not, and architecturally cannot, output HR-level employee evaluations or performance reviews.

## 1. Learning Mentor Core (`modules/learning_mentor`)
- **`PersonalLearningProfile`**: A strictly typed Pydantic schema tracking `completed_lessons`, `completed_sops`, and known `weak_areas`.
- **`SkillGapAnalyzer`**: Evaluates the user's Profile against their `Role Requirements`. If an operator is required to know Lockout/Tagout but hasn't completed the lesson, the Analyzer tags it as a gap.
- **`MentorFeatures`**: Uses the analyzed data to generate achievable, bite-sized daily goals (e.g., "Spend 15 mins reviewing the EAF Safety SOP").
- **`ManagerSupport`**: Allows managers to view aggregated team gaps and push specific learning modules into a user's mandatory queue.

## 2. Adaptive Learning Engine (`modules/adaptive_learning`)
- **`RoadmapAdapter`**: The dynamic router for learning paths. It receives the list of missing skills from the `SkillGapAnalyzer`. Crucially, it contains hardcoded prioritization logic that forces any module containing the keyword `safety` to the absolute front of the queue, ensuring compliance is always prioritized over general learning.
- **`AdaptiveLearningEngine`**: Orchestrates the adapter to output the top 3 "Next Best Actions" for the user.

## 3. Recommendation System (`modules/recommendations`)
- **`RecommendationEngine`**: Takes the raw adaptive output and translates it into UI-friendly payloads with explicit `priority_badges` and `action_types` (e.g., "Start Module").

## 4. Frontend Integration
The `MentorDashboard.jsx` is the visual command center.
- Uses a rich, dark-mode CSS implementation.
- Features the **Today's Goal** widget to immediately direct the user to their highest priority task.
- Features the **Action Required** widget. If the `SkillGapAnalyzer` finds a missing safety competency, this widget turns bright red to ensure the operator immediately addresses the gap before proceeding to optional learning.
