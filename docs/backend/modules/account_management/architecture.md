# Enterprise User Lifecycle & Policies Architecture

**Purpose**: Orchestrates the complex workflows governing how employees enter, move through, and exit the JSL Platform, enforced by an uncompromising central Policy Engine.

## 1. Account Management (`modules/account_management/`)
Controls the *state machine* of an employee.
- **`OnboardingRequest`**: Instead of instantly creating active users, JSL workflows require invitations. This tracks the email dispatch (placeholder) and temporary activation keys.
- **`ApprovalWorkflow`**: Not every account is auto-approved. A hierarchical structure allows a Manager to request an account, but forces the system to pause in a `PENDING_APPROVAL` state until the `dept_head_id` signs off.
- **`AuditLog`**: An immutable ledger of actions. If an account is suspended, the exact `actor_id` and timestamp is recorded natively.

## 2. Policy Engine (`modules/policies/`)
The central brain for evaluating complex cross-domain business rules.
- **Why decoupling?** Rather than littering HTTP controllers with `if request.user.role == 'Admin' or (request.user.role == 'Manager' and request.user.dept == target.dept)`, we encapsulate these into isolated, auditable Policy objects.
- **`RoleAssignmentPolicy`**: Ensures a Manager cannot assign a user a Role that has a higher `management_level` than their own.
- **`DepartmentTransferPolicy`**: Ensures a user cannot be moved between cost centers without bilateral sign-off from both Department Heads.

## 3. Core Domain Extensions (`users` & `organization`)
- **`EmployeeStatus`**: Expanded from basic 'ACTIVE' to encompass the entire HR reality (`LOCKED`, `ON_LEAVE`, `TRANSFERRED`, `EXITED`).
- **Matrix Management**: `ReportingHierarchy` now tracks entire JSON arrays for the `management_chain` and `approval_chain`, laying the foundation for complex nested routing required by multi-national enterprises.
