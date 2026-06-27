# Enterprise Knowledge Engine Architecture

## Overview
The Enterprise Knowledge Engine is the centralized heart of the learning platform. It shifts the paradigm from traditional "courses" to reusable **Knowledge Objects**. Everything the user learns—whether it is Manufacturing, Safety, SAP, SCADA, PLC, AI, SOPs, Equipment operations, Quality standards, Maintenance, or Future HR Learning—is represented as a discrete, scalable Knowledge Object.

## Knowledge Object Framework
A `KnowledgeObject` encapsulates a specific chunk of learning. By standardizing content into these objects, the platform achieves high reusability and enables advanced future capabilities like semantic search and AI-driven personalized learning paths.

### Core Properties
- **ID & Title**: Unique identifiers and descriptive names.
- **Content Type**: Defines the format (Interactive Lesson, PDF, Video, Simulation, AR/VR, 3D Model, etc.).
- **Metadata**: Categorization properties including Category, Department, Role, Difficulty, Estimated Time, Tags.
- **Relationships**: Defines how this object connects to others (Prerequisites, Related, Dependencies, Next Steps).
- **Lifecycle**: Strict version control (Draft, Review, Published, Archived) tracked by author and timestamps.
- **Payload**: The actual content data or references to external assets.

## Content Organization System
To organize thousands of Knowledge Objects efficiently, the platform utilizes a `ContentGroup` framework. A `ContentGroup` can represent various organizational structures:
- **Categories**
- **Topics & Subtopics**
- **Collections & Playlists**
- **Learning Paths**
- **Manufacturing Stages**
- **Department & Role Libraries**

Groups can be hierarchical (using `parent_id`) and contain ordered references to Knowledge Objects (`object_ids`).

## Content Versioning
The Knowledge Engine supports content versioning through a strict lifecycle workflow:
1. **Drafting**: Content is cloned or created anew as a `DRAFT`.
2. **Reviewing**: Moving to `REVIEW` triggers workflows (to be fully integrated later).
3. **Publishing**: Marking as `PUBLISHED` makes it available in the global engine.
4. **Archiving**: Older versions or obsolete content are transitioned to `ARCHIVED`.

## Learning Experience Framework
The `LearningExperience` acts as a structured wrapper for presenting a `KnowledgeObject` to the end-user. It standardizes the consumption format across the platform.

### Supported Elements
- **Overview & Objectives**: Clear statements of intent and goals.
- **Learning Content**: The interactive component or media (pulled from the Knowledge Object).
- **Important Notes, Warnings, Safety Alerts**: Crucial contextual information dynamically surfaced to the user.
- **Knowledge Check**: Assessments linked to the material.
- **Summary & Related Topics**: Consolidating the learning and guiding the next steps.
- **References**: External materials and deep links.
- **AI Chat (Future)**: Prepared flag to enable contextual AI tutoring embedded in the experience.

## Search Architecture
The platform is designed to support deep multidimensional search. While initial implementation supports tag, role, and department filtering, the architecture is prepared for:
- Global Search
- Department/Role/Equipment scoped Search
- **Future AI/Semantic Search**: Vector embeddings can be generated from the `KnowledgeObject`'s text payloads and stored in vector databases (tracked via the `ai_embeddings_indexed` flag).

## Future AI Integration
- **Indexing**: All Knowledge Objects will be periodically ingested and embedded into a vector store.
- **AI Conversations**: Interactive lessons can be entirely driven by `AI_CONVERSATION` ContentTypes.
- **Adaptive Paths**: The engine's granular nature (Knowledge Objects + Relationships) provides the perfect training set for AI to dynamically construct Learning Paths (`ContentGroups`) tailored to real-time user performance.
