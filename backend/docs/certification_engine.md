# Enterprise Certification, Achievement & Digital Credential Platform

## Overview
The Credential Platform (Enterprise Implementation Plan 3.7) provides a formalized mechanism to reward, track, and verify learning outcomes. Rather than issuing certificates based purely on lesson completion, this architecture ties issuance directly to verified competency, managerial approval, and specific learning journey milestones. 

## Architectural Separation
The credential ecosystem is divided into three distinct modules to manage separate concerns cleanly:

### 1. Certificates Module
Handles formal enterprise-grade certificates.
- **CertificateTemplate**: Acts as the blueprint. It defines validity periods (e.g., expires in 365 days) and houses complex `EligibilityRule`s.
- **Eligibility Rules**: A user cannot request a certificate until they meet strict criteria (e.g., minimum assessment scores, completion of mandatory lessons, and achieving a specific threshold in a `CompetencyArea`).
- **Lifecycle**: The `CertificateEngine` oversees the transition of a `Certificate` from `PENDING_APPROVAL` (if HR or Manager sign-off is needed) to `ACTIVE`. It also handles revocation and expiration logic.

### 2. Achievements Module
Handles automated, gamified learning milestones.
- **Milestones**: Includes `LEARNING_MILESTONE`, `DEPARTMENT_MILESTONE`, `PERFECT_SCORE`, and `FAST_LEARNER`.
- **Unlock Logic**: The `AchievementEngine` automatically awards these based on triggers from the `ProgressEngine` (e.g., completing 10 lessons in a week).

### 3. Credentials Module
Handles granular skill badging and the public verification architecture.
- **DigitalBadges**: Smaller, focused skill markers (e.g., `SAFETY_BADGE`, `INNOVATION_BADGE`).
- **Competency Levels**: Badges can map directly to levels (`BEGINNER`, `INTERMEDIATE`, `ADVANCED`, `EXPERT`, `TRAINER`).
- **VerificationEngine**: Exposes methods that accept a `certificate_number` or badge ID and returns a `CredentialVerification` payload. This payload confirms validity, issuance date, and expiration status, serving as the backend layer for future public verification portals or QR code scans.

## Future Enterprise Integration
- **Digital Signatures**: The backend models support attaching external verification URLs and hashes.
- **Public QR Verification**: The `CredentialVerification` payload is designed specifically to act as the JSON response for a public unauthenticated route (e.g., `GET /api/public/verify/{id}`) when someone scans a printed QR code.
