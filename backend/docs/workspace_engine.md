# Personalized Role-Based Workspaces & Department Experience

## Overview
The Workspace Engine (Enterprise Implementation Plan 3.9) acts as the contextual presentation layer for the entire digital learning platform. It dynamically morphs the frontend experience so that every authenticated user receives a dedicated application tailored strictly to their Role, Department, and Learning Progress.

## Workspace Engine Architecture
The `WorkspaceEngine` operates as a middleware orchestrator sitting right after authentication. Before the frontend renders anything, it queries this engine for a `WorkspaceContext` payload.

### The Workspace Context Payload
The `WorkspaceContext` is a monolithic payload containing all the structural scaffolding needed to render the UI for that specific user:
1. **NavigationMenu**: A dynamically generated hierarchy (`NavigationItem`s). It natively hides or shows links based on `RoleType` and `DepartmentType`. For example, an `OPERATOR` in `PRODUCTION` gets Quick Links to the Production SOP Library, while a `DEPARTMENT_HEAD` in `QUALITY` gets links to Approvals and Analytics.
2. **Active Announcements**: A filtered array of `Announcement` models. Announcements can be targeted globally (`ORGANIZATION` wide) or scoped tightly to a `RoleType` (e.g., only managers see it) or `DepartmentType`.
3. **DepartmentLandingPage**: If the user belongs to a recognized department, the engine provides specific overview texts, targeted featured roadmaps, and deep links to their Equipment/SOP libraries.

## Role Visibility Mapping
Visibility logic (`VisibilityLevel` enum) is deeply ingrained. Any navigation item or widget can be set to:
- `VISIBLE`: Standard access.
- `HIDDEN`: Stripped from the payload entirely.
- `READ_ONLY`: Visible but disabled (e.g., for `VISITOR`s or lower-tier roles observing analytics).
- `EDITABLE`: Full access.
- `APPROVAL_REQUIRED`: Triggers workflows to managers before granting access.

## Department Experiences
The engine is preconfigured with the standard Enterprise departments (e.g., `AUTOMATION`, `IT`, `STEEL_MELTING_SHOP`). 
By utilizing the `DepartmentLandingPage` structure, the engine ensures that a Steel Melting Shop worker never sees the default IT helpdesk roadmaps, but instead is immediately greeted with Safety Protocols and Mechanical Equipment manuals upon login.

## Integration with Dashboard Engine
The `WorkspaceEngine` works in tandem with the `DashboardEngine` (Implementation Plan 3.8). While the Dashboard handles the granular grid layout of the individual widgets, the Workspace Engine passes down the defining `RoleType` and `DepartmentType` contexts so the Dashboard can accurately fetch the right default widget configurations.

## Future AI Personalization
In the future, the `WorkspaceContext` can be intercepted by an AI Personalization Engine that automatically rewrites navigation labels, dynamically pins modules a user frequently visits, or crafts AI-generated summary announcements tailored just for them.
