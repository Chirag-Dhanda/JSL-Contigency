# Stage 5.8: Enterprise Discovery Engine

This document outlines the architecture for the Enterprise Discovery Engine, replacing hardcoded navigation with a dynamic, graph-based knowledge explorer.

## 1. Discovery Engine Service (`modules/discovery_engine/`)
The `DiscoveryEngineService` is the central brain for navigation. When a user requests to view any entity (e.g., a piece of Equipment, a Department, an SOP), this service queries both the `MetadataEngine` and the `RelationshipEngine`.
- **Breadcrumbs**: It automatically traces `BELONGS_TO` edges upwards to build a hierarchical navigation path (e.g., Plant -> Department -> Equipment).
- **Related Objects**: It performs a 1-degree graph traversal in all directions, grouping related nodes into logical buckets (`parents`, `children`, `equipment`, `sops`, `lessons`, etc.).

## 2. Universal Hyperlink Engine (`modules/hyperlink_engine/`)
The `HyperlinkEngineService` is a utility designed to inject interconnectedness into unstructured text. It scans strings (such as AI-generated summaries or text documents) and dynamically replaces known Entity Names with Markdown hyperlinks pointing directly into the `KnowledgeExplorer`. 
- This guarantees that AI conversations are never dead ends; if the AI mentions "Electric Arc Furnace", the user can click it to immediately view its full metadata profile.

## 3. Frontend Knowledge Explorer (`modules/knowledge_explorer/`)
- **ExplorerLayout**: A dynamic route wrapper (`/explore/:entityId`) that fetches the unified Discovery Profile for any given entity.
- **SmartEntityPage**: A universal component capable of rendering any object type. It automatically organizes the entity's attributes and renders visually appealing cards for every connected object in the graph. It also hosts the `BreadcrumbEngine` for easy hierarchical navigation.
- **Recommendations**: The right sidebar calculates and displays "AI Recommendations" based on the entity's context, providing "Next Best Actions" (like viewing a related workflow or reading a recent ticket).
