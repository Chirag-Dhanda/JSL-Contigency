# Knowledge Engine Architecture

**Purpose**: The central brain of the JSL platform. It stores, versions, and serves reusable educational content (`KnowledgeObject`) to decoupled presentation engines like the Learning Roadmap or the Digital Factory.

## 1. Core Abstractions (`modules/knowledge/models.py`)

### `KnowledgeObject`
This is the atomic unit of learning in the platform. Rather than building a rigid "Course", authors create discrete `KnowledgeObjects`.
- **Content Types**: Supports Interactive Lessons, PDFs, Videos, Quizzes, and future AI Conversations.
- **Metadata Tagging**: Strongly typed `tags`, `difficulty`, `department`, and `role` fields allow dynamic, personalized queries.
- **Versioning & Status**: Every object moves through a strict lifecycle: `DRAFT` -> `REVIEW` -> `PUBLISHED` -> `ARCHIVED`. Only published content is visible to standard employees.

### `KnowledgeRelationship`
Knowledge doesn't exist in a vacuum. Objects can reference other objects.
- Defines strict prerequistes or "Related Content" to dynamically generate learning paths.

## 2. Knowledge Service (`modules/knowledge/service.py`)
- **Authoring Lifecycle**: Manages the creation of drafts and the transition matrix to publish them.
- **Search Abstraction**: Currently implementing a mock text/tag search algorithm. This is the exact integration point where future Semantic Search (via vector databases and LLM embeddings) will be injected.

## 3. Interactive Learning Viewer (`frontend/modules/learning/`)
To visualize how a `KnowledgeObject` is consumed, we built a premium UI prototype.
- **Structured Content Blocks**: The UI is divided into semantic sections (Objectives, Content, Knowledge Check).
- **Interactive Feedback**: A mock "Knowledge Check" quiz is implemented in vanilla JavaScript. Answering incorrectly temporarily locks the button, whereas answering correctly unlocks the DAG Engine progression button.
- **Safety Alerts**: Custom CSS styles render critical safety warnings (`alert-block safety-alert`) with distinct visual prominence to adhere to heavy industry compliance standards.
