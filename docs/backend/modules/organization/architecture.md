# Organization Hierarchy & User Domain Architecture

**Purpose**: The single source of truth for the Process-Contingency-JSL enterprise structure, decoupling authentication credentials from complex HR reporting chains.

## 1. User Domain (`modules/users/`)
Focuses on the generic profile of the employee.
- **`UserEntity`**: The root aggregate linking to Authentication, Departments, Roles, and external identifiers (SAP, LDAP).
- **`EmployeeProfile`**: Contains PII (Personally Identifiable Information) like names, locations, and timezones.
- **`EmployeeMetadata`**: An unstructured schema block (`Dict[str, Any]`) permitting arbitrary preference or temporary state tracking without requiring database migrations.
- **Services**: `EmployeeDirectoryService` handles profile lookups, while `ManagerService` handles direct-report querying.

## 2. Organization Domain (`modules/organization/`)
Focuses strictly on the structural hierarchy of JSL.
- **`Department`**: A recursive tree structure mapping Parent and Child departments, complete with internal `sap_cost_center` mapping.
- **`Role`**: *NOT* an Enum. A dynamic configuration table allowing administrators to create new roles (e.g., *Deputy General Manager*, *Executive Engineer*) on the fly and assign them a `management_level` for implicit permissions.
- **`ReportingHierarchy`**: Replaces simple `manager_id` with a complex matrix allowing an employee to have an `approver_id` for leave requests and a separate `escalation_id` for compliance failures.

## 3. The Decoupling Strategy
Why aren't these in the Authentication module?
Authentication's sole job is to verify identity and return a JWT. 
The User/Organization domains handle the *business reality* of the identity. An employee's status can be `ACTIVE` in AD, but their JSL `EmployeeStatus` may be `PENDING_ONBOARDING`, blocking them from enterprise features until HR clears them.

By mapping `role_id` and `department_id` in the `UserEntity`, the system is ready to synchronize natively with a future external HRMS (Human Resource Management System) API.
