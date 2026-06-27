# Enterprise Authorization Architecture

**Purpose**: An advanced multi-layered security engine governing "who can do what" across the JSL platform. It seamlessly merges Role-Based Access Control (RBAC) with Department-Based Access Control (DBAC).

## 1. Permissions Taxonomy (`modules/permissions/`)
Handles the definition of rights.
- **`AccessLevel`**: Configurable severity levels (`READ`, `UPDATE`, `APPROVE`, `ADMINISTER`).
- **`Permission`**: A discrete right (e.g., `document.approve`, `user.create`).
- **`RolePermissionMapping`**: A mapping entity joining roles to permissions. It uniquely supports `is_revoked`, enabling administrators to grant a broad role but explicitly deny a specific nested permission for a specific sub-role without creating entirely new role definitions.

## 2. Authorization Pipeline (`modules/authorization/`)
Handles the evaluation of rights. The `AuthorizationPipeline.evaluate_access()` sequence:

1. **Role Resolution (RBAC)**: Validates if the user's assigned roles explicitly contain the `Permission` required.
2. **Department Resolution (DBAC)**: Every secure entity holds a `ResourceOwnership` block tracking `owned_by_dept_id`. By default, even with correct RBAC roles, a user is restricted from interacting with resources outside their department.
3. **Hierarchy Validation**: Checks if the user falls on the correct side of the reporting chain (e.g., a Manager can modify their direct reports, but direct reports cannot modify their Manager).
4. **Cross-Department Exceptions**: If a DBAC failure occurs, the engine checks for active `CrossDepartmentAccess` records granting temporary or specific bridges across JSL departments.

## 3. Strict Policies
Complex business rules are defined as explicit `Policy` classes (e.g., `AccountCreationPolicy`, `DocumentApprovalPolicy`) rather than hardcoded `if/else` statements scattered throughout the codebase. This allows them to be audited and unit-tested in isolation.
