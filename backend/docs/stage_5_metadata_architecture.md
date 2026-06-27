# Stage 5.1: Enterprise Metadata Architecture

This document outlines the foundation of Stage 5, transitioning the platform from fixed SQL schemas to a dynamic, JSON-backed Entity-Attribute-Value (EAV) system.

## 1. The Entity Framework (`modules/entity_framework/`)
The `EnterpriseEntity` replaces all prior fixed models (like Department, Station, WorkCenter). It is a generalized wrapper holding:
- **Core Identity**: `id`, `name`, `entity_type`
- **Dynamic Payload**: `metadata` (A JSON dictionary containing all custom properties).
- **System Indexes**: `ai_metadata`, `search_metadata` for fast retrieval.
- **State Control**: `status` (Draft, Published, etc.), `version`, `permission_profile`.

## 2. The Entity Registry (`modules/entity_registry/`)
Because entities are dynamic, the platform needs a way to enforce rules. The `EntityRegistryService` holds `EntityTypeDefinition`s.
- An admin can register a new type (e.g., `iot_sensor`) without writing code.
- They define a `metadata_schema` (e.g., "temperature must be a number > 0").
- The registry acts as the source of truth for what a dynamic entity is allowed to look like.

## 3. Schema & Validation Engine (`modules/schema_engine/`)
The `SchemaValidator` is the enforcer. When a user tries to create or update an entity, the validator checks the dynamic `metadata` payload against the rules stored in the registry.
- Checks required fields.
- Checks data types (string, number, boolean, list).
- Checks min/max constraints and enum sets.
- If validation fails, it throws a `SystemException`.

## 4. Metadata Engine (`modules/metadata_engine/`)
The master orchestrator exposing the API. It ties the framework, registry, and schema validator together.
- `create_entity()`: Looks up schema -> Merges defaults -> Validates -> Instantiates Entity.
- `update_entity_metadata()`: Validates new partial data -> Merges -> Bumps version.

## 5. Future Extension Strategy
By decoupling the data schema from the database architecture, the JSL Contingency platform is now ready to ingest any future business object (SAP Work Orders, SCADA tags, PLC metrics) dynamically. We simply register the new `EntityTypeDefinition` via API, and the system instantly supports it.
