# Enterprise Access Governance Architecture

**Purpose**: Implements the strict workflows governing how JSL employees request, receive, and forfeit elevated permissions across departmental boundaries.

## 1. Access Request Core (`modules/access_request/`)
Handles the lifecycle of an `AccessRequestEntity`.
- **States**: `PENDING` -> `APPROVED` -> `EXPIRED`.
- **Duration**: By default, requests are tracked as `TEMPORARY`. Once the `expires_at` threshold is passed, the `AccessRequestService` automatically drops the grant during lazy evaluation, ensuring zero orphan privileges remain active in the system.

## 2. Dynamic Authorization Engine (`modules/authorization/`)
The `AuthorizationPipeline` was completely overhauled to evaluate temporary overlays:
1. **RBAC Check**: "Does the user possess the abstract permission?"
2. **DBAC Fast Path**: "Does the user belong to the same department as the resource?" If yes, full access.
3. **Cross-Department Temporary Grant**: If DBAC fails, the engine queries the `AccessRequestService` for active temporary grants targeting the exact resource. If valid, full access.
4. **Overview Access Fallback**: If no temporary grant exists, but the user is authenticated and RBAC permits it, the system yields an "Overview Access" flag. This allows controllers to return scrubbed, high-level JSON (e.g., Department Name) instead of sensitive operational data.

## 3. Centralized Audit & Notifications (`modules/audit/`, `modules/notifications/`)
- Every Access Request creation and approval is logged directly to the immutable `AuditService` ledger.
- `NotificationHooks` capture the exact timestamp of these events, preparing the system to dispatch real-time alerts (via Microsoft Teams or Email) whenever someone attempts to access restricted SAP resources or cross-department dashboards.
