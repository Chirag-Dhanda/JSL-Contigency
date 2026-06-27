# Enterprise Authentication Flow & Security Controls

**Purpose**: Implements the strict access pipelines, enforcing security controls (lockouts, forced password resets) natively before tokens are ever minted.

## 1. The Strict Login Sequence (`AuthService.login()`)
The login process is an unyielding, linear state-machine:
1. **Pre-Check (AccountLockoutService)**: Checks if the username has failed >5 times in the last 15 minutes. Blocks immediately if true.
2. **Entity Lookup**: Mocks a DB lookup. If not found, triggers a false-failure and logs `FAILED_NOT_FOUND`.
3. **Cryptographic Verification**: `PasswordHasher` runs bcrypt evaluation.
4. **Status Verification**: Blocks `LOCKED` and `SUSPENDED` profiles.
5. **Policy Verification**: Checks if `force_change` is set (true for First Time Logins). If true, strictly throws a `403 FORBIDDEN` and logs `FORCE_CHANGE_REQUIRED`.
6. **Token Dispensation**: Generates `access_token` and `refresh_token` using `JWTService` containing a unique `jti`.
7. **Session Registration**: Commits the `jti` to the `SessionManager` state storage.
8. **Audit Logging**: Saves a `SUCCESS` event in the `LoginHistory` ledger.

## 2. Security Controls (`modules/security/`)
- **`AccountLockoutService`**: A naive brute-force preventer. Tracks attempts against usernames (not IPs, as an IP lock could block an entire department via NAT, while a username lock is targeted).
- **`PasswordRecoveryService`**: Generates short-lived (15 minute), single-use UUID tokens for password recovery, mocking email dispatch.

## 3. First Login & State Traversal
When HR provisions an account via `AccountManagementModule`, they receive a temporary password. Logging in forces a `403`. The user must submit to `/change-password` using the temporary password, which clears the `force_change` flag and transitions their state to `ACTIVE`, allowing standard JWT issuance.
