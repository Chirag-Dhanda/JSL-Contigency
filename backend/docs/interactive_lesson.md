# Interactive Lesson Workspace Architecture

## Overview
The Interactive Lesson Workspace is a core component of the Digital Learning Experience (Enterprise Implementation Plan 3.4). It marks a departure from static content pages to dynamic, interactive, and modular workspaces. This architecture enables progress tracking, personalization, complex layouts, and seamless future AI integrations.

## Lesson Workspace
The `LessonWorkspace` is the top-level container for a digital lesson. 

### Core Components
- **Lesson Header**: Contains the lesson title, contextual metadata, and overall progress.
- **Lesson Navigation**: (`LessonNavigation` model) Supports Table of Contents, Breadcrumbs, Previous/Next lesson mapping, and jump-to functionality.
- **Content Viewer**: An ordered array of `ContentBlock` models that represent the actual lesson material.
- **Lesson Footer**: (`LessonFooter` model) Displays a summary, achieved objectives, related lessons, and upcoming assessments (e.g., quizzes).

## Modular Content Block System
Instead of a single monolithic HTML string, lessons are built using the `ContentBlock` architecture. This polymorphic system utilizes Pydantic discriminated unions on the backend and mapped TypeScript interfaces on the frontend.

### Supported Block Types (`type` discriminator)
- **Text & Media**: `HEADING`, `PARAGRAPH`, `RICH_TEXT`, `IMAGE`, `IMAGE_GALLERY`, `VIDEO`, `PDF_VIEWER`, `TABLE`.
- **Interactive & Manufacturing**: `TIMELINE`, `FLOW_DIAGRAM`, `EQUIPMENT_DIAGRAM`, `PROCESS_ANIMATION`.
- **Advanced (Future)**: `CODE`, `INTERACTIVE_SIMULATION`, `AI_DISCUSSION`.

### Interactive Components
In addition to blocks, lessons support interactive micro-components:
- `KnowledgeCard`: Small, bite-sized info cards (can be marked safety critical).
- `QuickFact`, `SafetyAlert`, `EngineeringTip`, `ImportantWarning`.
- `ExpandableSection` and `Accordion`: For nested, optional, or deep-dive content.

## Learner Tools
The workspace maintains user-specific state via the `LearnerTools` model.
- **Progress Tracking**: Tracks reading progress percentage and estimates time remaining.
- **Personalization**: Users can configure Theme (`LIGHT`/`DARK`), Font Size, and Accessibility Modes.
- **Interactions**: Supports Bookmarking specific `ContentBlock` IDs, taking Personal Notes on specific blocks, highlighting text, and marking lessons as favourites.

## Responsive Lesson Layout
While the frontend UI is built independently, the architecture is designed to support:
- **Desktop/Laptop**: Full multi-column view (sidebar navigation, main content, right-side tools).
- **Tablet/Mobile**: Collapsible sidebars, bottom navigation, and stacked content blocks.
- **Fullscreen/Print**: Clean reading modes omitting sidebars and tools.

## Future AI Integration
The block system and workspace are inherently designed for AI:
- **AIDiscussionBlock**: A dedicated block type designed to host inline AI chat components.
- **Contextual Prompts**: The structured nature of `ContentBlock`s allows tools like "Explain Simpler", "Explain Technically", or "Generate Notes" to pull specific block IDs rather than full document strings.
- **Translation**: Block-level text properties can be translated independently while preserving layout structures (like images and diagrams).
