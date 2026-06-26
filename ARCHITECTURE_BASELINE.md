# Architecture Baseline
**Overall Architecture**: Clean Architecture, Layered.
**Module Boundaries**: Hard isolation between domains (e.g. auth, users, learning, sap, ai).
**Repository Organization**: Monorepo with strictly governed top-level domains.
**Naming Standards**: kebab-case for folders, PascalCase for classes, snake_case/camelCase per language convention.
**Documentation Standards**: Single Source of Truth (SSOT) via `docs/`, `governance/` and extensive READMEs.
**Dependency Philosophy**: Strict Dependency Inversion; core logic must not depend on external frameworks or databases.
**Security Philosophy**: Security-first, explicit JWT/RBAC/DBAC, zero-trust internal layers.
**Scalability Philosophy**: Stateless services ready for horizontal scaling, microservices-ready boundaries.
**Maintainability Philosophy**: High cohesion, low coupling. Enforced by architectural checklists and reviews.
