"""
database/models.py
─────────────────────────────────────────────────────────────────
SQLAlchemy ORM table definitions for EKOS EP-01.

Design decisions:
  • enterprise_entities stores the FULL EnterpriseEntity pydantic model as
    JSONB in `payload`. Indexed columns (id, entity_type, status, created_by)
    are promoted to real columns for efficient querying.
  • entity_type_definitions stores the FULL EntityTypeDefinition as JSONB.
  • enterprise_relationships mirrors the same pattern.
  • users, roles, role_assignments, sessions, audit_log are added for EP-02.
    They are created now so the schema is coherent from day one.
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime,
    Text, ForeignKey, Index, UniqueConstraint, Float
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from database.engine import Base
try:
    from pgvector.sqlalchemy import Vector  # type: ignore
    _VECTOR_AVAILABLE = True
except ImportError:
    Vector = None  # type: ignore
    _VECTOR_AVAILABLE = False



def _now():
    return datetime.now(timezone.utc)


# ─────────────────────────────────────────────
# Object Designer / Type Registry
# ─────────────────────────────────────────────

class DbEntityTypeDefinition(Base):
    """
    Stores dynamic object type definitions (the "schema templates").
    Platform source-of-truth for what kinds of enterprise objects exist.
    """
    __tablename__ = "entity_type_definitions"

    type_id = Column(String(128), primary_key=True)
    display_name = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="Draft")   # Draft|Review|Published|Deprecated
    version = Column(Integer, nullable=False, default=1)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_now, onupdate=_now)

    # Full definition stored as JSONB (validation rules, ui_schema, etc.)
    payload = Column(JSONB, nullable=False, default=dict)

    __table_args__ = (
        Index("ix_etd_status", "status"),
        Index("ix_etd_is_active", "is_active"),
    )

class DbEntityTypeVersion(Base):
    """
    Immutable version history of entity type definitions.
    Used for rollbacks, audit trails, and retrieving past schemas.
    """
    __tablename__ = "entity_type_versions"

    id = Column(String(64), primary_key=True, default=lambda: f"etv-{uuid.uuid4().hex[:12]}")
    type_id = Column(String(128), ForeignKey("entity_type_definitions.type_id", ondelete="CASCADE"), nullable=False)
    version = Column(Integer, nullable=False)
    status = Column(String(32), nullable=False)
    payload = Column(JSONB, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_now)
    created_by = Column(String(128), nullable=False, default="system")

    __table_args__ = (
        UniqueConstraint("type_id", "version", name="uq_type_version"),
        Index("ix_etv_type_id", "type_id"),
    )


# ─────────────────────────────────────────────
# Enterprise Entities (core metadata objects)
# ─────────────────────────────────────────────

class DbEnterpriseEntity(Base):
    """
    Every dynamic business object (Department, Equipment, SOP, etc.).
    The `payload` JSONB column holds the full EnterpriseEntity structure.
    """
    __tablename__ = "enterprise_entities"

    id = Column(String(64), primary_key=True, default=lambda: f"ent-{uuid.uuid4().hex[:12]}")
    name = Column(String(512), nullable=False)
    entity_type = Column(String(128), nullable=False)
    display_name = Column(String(512), nullable=False)
    status = Column(String(32), nullable=False, default="DRAFT")
    version = Column(Integer, nullable=False, default=1)
    created_by = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_now)
    modified_at = Column(DateTime(timezone=True), nullable=False, default=_now, onupdate=_now)

    # Full pydantic payload stored as JSONB
    payload = Column(JSONB, nullable=False, default=dict)

    __table_args__ = (
        Index("ix_ee_entity_type", "entity_type"),
        Index("ix_ee_status", "status"),
        Index("ix_ee_created_by", "created_by"),
        # GIN index for full JSONB traversal / containment queries
        Index("ix_ee_payload_gin", "payload", postgresql_using="gin"),
        # Full-text search vector index on name + display_name
        # Built via a generated column in migration for production; using index here for now
        Index("ix_ee_name", "name"),
        Index("ix_ee_display_name", "display_name"),
    )


# ─────────────────────────────────────────────
# Relationship Type Registry
# ─────────────────────────────────────────────

class DbRelationshipTypeDefinition(Base):
    __tablename__ = "relationship_type_definitions"

    type_id = Column(String(128), primary_key=True)
    display_name = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    is_directed = Column(Boolean, nullable=False, default=True)
    is_active = Column(Boolean, nullable=False, default=True)
    payload = Column(JSONB, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_now)


# ─────────────────────────────────────────────
# Enterprise Relationships
# ─────────────────────────────────────────────

class DbEnterpriseRelationship(Base):
    """
    Every directional or bidirectional link between enterprise entities.
    PostgreSQL is the system of record; Neo4j is the projection layer (EP-05).
    """
    __tablename__ = "enterprise_relationships"

    id = Column(String(64), primary_key=True, default=lambda: f"rel-{uuid.uuid4().hex[:12]}")
    source_entity_id = Column(String(64), nullable=False)
    target_entity_id = Column(String(64), nullable=False)
    relationship_type = Column(String(128), nullable=False)
    direction = Column(String(32), nullable=False, default="DIRECTED")
    created_by = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_now)
    rel_metadata = Column(JSONB, nullable=False, default=dict)

    __table_args__ = (
        Index("ix_er_source", "source_entity_id"),
        Index("ix_er_target", "target_entity_id"),
        Index("ix_er_type", "relationship_type"),
        Index("ix_er_source_type", "source_entity_id", "relationship_type"),
    )


# ─────────────────────────────────────────────
# Users, Roles, Sessions  (EP-02 foundation)
# ─────────────────────────────────────────────

class DbUser(Base):
    __tablename__ = "users"

    id = Column(String(64), primary_key=True, default=lambda: f"usr-{uuid.uuid4().hex[:12]}")
    email = Column(String(256), nullable=False, unique=True)
    username = Column(String(128), nullable=False, unique=True)
    full_name = Column(String(256), nullable=True)
    hashed_password = Column(String(256), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    department_id = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_now, onupdate=_now)
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_users_email", "email"),
        Index("ix_users_username", "username"),
    )


class DbRole(Base):
    __tablename__ = "roles"

    id = Column(String(64), primary_key=True, default=lambda: f"role-{uuid.uuid4().hex[:8]}")
    name = Column(String(64), nullable=False, unique=True)   # PLATFORM_ADMIN, MASTER_EDITOR …
    description = Column(Text, nullable=True)
    permissions = Column(JSONB, nullable=False, default=list)
    is_system_role = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_now)


class DbRoleAssignment(Base):
    __tablename__ = "role_assignments"

    id = Column(String(64), primary_key=True, default=lambda: f"ra-{uuid.uuid4().hex[:8]}")
    user_id = Column(String(64), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(String(64), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    assigned_by = Column(String(64), nullable=True)
    assigned_at = Column(DateTime(timezone=True), nullable=False, default=_now)

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uq_user_role"),
        Index("ix_ra_user_id", "user_id"),
    )


class DbSession(Base):
    """JWT session tracking for revocation (JTI blocklist)."""
    __tablename__ = "sessions"

    jti = Column(String(128), primary_key=True)
    user_id = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_now)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, nullable=False, default=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_sessions_user_id", "user_id"),
        Index("ix_sessions_revoked", "revoked"),
    )


# ─────────────────────────────────────────────
# Audit Log  (EP-13 foundation — immutable)
# ─────────────────────────────────────────────

class DbAuditLog(Base):
    """
    Append-only audit log. Rows must never be deleted or updated.
    Enforced at the DB level via trigger in production (added in EP-13 migration).
    """
    __tablename__ = "audit_log"

    id = Column(String(64), primary_key=True, default=lambda: f"aud-{uuid.uuid4().hex[:12]}")
    user_id = Column(String(128), nullable=False)
    entity_id = Column(String(128), nullable=True)
    module = Column(String(128), nullable=False)
    action = Column(String(128), nullable=False)
    old_value = Column(JSONB, nullable=True)
    new_value = Column(JSONB, nullable=True)
    reason = Column(Text, nullable=True)
    ip_address = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_now)

    __table_args__ = (
        Index("ix_audit_entity_id", "entity_id"),
        Index("ix_audit_user_id", "user_id"),
        Index("ix_audit_action", "action"),
        Index("ix_audit_created_at", "created_at"),
    )


# ─────────────────────────────────────────────
# EP-05: Knowledge Platform
# ─────────────────────────────────────────────

class DbKnowledgeAsset(Base):
    """
    Master record for any document, manual, SOP, or policy ingested into EKOS.
    PostgreSQL is the authoritative store. Neo4j holds the relationship projection.
    """
    __tablename__ = "knowledge_assets"

    id = Column(String(64), primary_key=True, default=lambda: f"ka-{uuid.uuid4().hex[:12]}")
    title = Column(String(512), nullable=False)
    asset_type = Column(String(128), nullable=False)       # SOP, POLICY, MANUAL, PROCEDURE, REFERENCE, etc.
    source_filename = Column(String(512), nullable=True)
    source_uri = Column(String(1024), nullable=True)
    status = Column(String(32), nullable=False, default="DRAFT")  # DRAFT|INGESTING|REVIEW|PUBLISHED|ARCHIVED
    version = Column(Integer, nullable=False, default=1)
    language = Column(String(16), nullable=False, default="en")
    entity_type_ref = Column(String(128), nullable=True)   # Link to an EntityTypeDefinition if applicable
    department_owner = Column(String(128), nullable=True)
    created_by = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_now, onupdate=_now)
    published_at = Column(DateTime(timezone=True), nullable=True)
    archived_at = Column(DateTime(timezone=True), nullable=True)

    # Full asset metadata payload (JSONB)
    extracted_metadata = Column(JSONB, nullable=False, default=dict)
    ontology_tags = Column(JSONB, nullable=False, default=list)  # Approved ontology mappings
    acl = Column(JSONB, nullable=False, default=dict)            # Access control: {roles: [], departments: []}

    __table_args__ = (
        Index("ix_ka_status", "status"),
        Index("ix_ka_asset_type", "asset_type"),
        Index("ix_ka_department", "department_owner"),
        Index("ix_ka_created_by", "created_by"),
        Index("ix_ka_entity_type_ref", "entity_type_ref"),
    )


class DbKnowledgeChunk(Base):
    """
    One paragraph/section chunk from a KnowledgeAsset.
    Stores the text AND the pgvector embedding for semantic retrieval.
    """
    __tablename__ = "knowledge_chunks"

    id = Column(String(64), primary_key=True, default=lambda: f"kc-{uuid.uuid4().hex[:12]}")
    asset_id = Column(String(64), ForeignKey("knowledge_assets.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(Integer, nullable=False)         # Positional index within parent asset
    chunk_strategy = Column(String(64), nullable=False, default="fixed")  # fixed|paragraph|heading|semantic
    text = Column(Text, nullable=False)
    char_start = Column(Integer, nullable=True)           # Character offset in source text
    char_end = Column(Integer, nullable=True)
    token_count = Column(Integer, nullable=True)
    chunk_metadata = Column(JSONB, nullable=False, default=dict)
    # pgvector column — 768 dimensions (nomic-embed-text / similar)
    embedding = Column(Vector(768) if _VECTOR_AVAILABLE and Vector is not None else JSONB, nullable=True)
    embedding_model = Column(String(128), nullable=True)
    embedding_version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_now)

    __table_args__ = (
        Index("ix_kc_asset_id", "asset_id"),
        Index("ix_kc_chunk_index", "asset_id", "chunk_index"),
    )


class DbIngestionJob(Base):
    """
    Tracks every document through the full ingestion lifecycle pipeline.
    Each stage updates this record.
    """
    __tablename__ = "ingestion_jobs"

    id = Column(String(64), primary_key=True, default=lambda: f"job-{uuid.uuid4().hex[:12]}")
    asset_id = Column(String(64), ForeignKey("knowledge_assets.id", ondelete="SET NULL"), nullable=True)
    filename = Column(String(512), nullable=False)
    file_type = Column(String(64), nullable=False)
    file_size_bytes = Column(Integer, nullable=True)
    status = Column(String(32), nullable=False, default="QUEUED")
    # QUEUED|VALIDATING|PARSING|CHUNKING|EXTRACTING|ONTOLOGY_MAPPING|EMBEDDING|REVIEW|COMPLETED|FAILED
    current_stage = Column(String(64), nullable=True)
    progress_pct = Column(Integer, nullable=False, default=0)
    submitted_by = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_now, onupdate=_now)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    stage_log = Column(JSONB, nullable=False, default=list)  # [{stage, status, ts, msg}]

    __table_args__ = (
        Index("ix_ij_status", "status"),
        Index("ix_ij_submitted_by", "submitted_by"),
        Index("ix_ij_asset_id", "asset_id"),
    )


class DbOntologyCandidate(Base):
    """
    A suggested mapping between a knowledge asset and an ontology concept.
    Requires Master Editor approval before becoming authoritative.
    """
    __tablename__ = "ontology_candidates"

    id = Column(String(64), primary_key=True, default=lambda: f"oc-{uuid.uuid4().hex[:12]}")
    asset_id = Column(String(64), ForeignKey("knowledge_assets.id", ondelete="CASCADE"), nullable=False)
    concept_id = Column(String(128), nullable=False)
    concept_label = Column(String(256), nullable=False)
    confidence = Column(Float, nullable=False, default=0.0)
    source_text_snippet = Column(Text, nullable=True)    # The text that triggered this suggestion
    status = Column(String(32), nullable=False, default="PENDING")  # PENDING|APPROVED|REJECTED
    reviewed_by = Column(String(128), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_now)

    __table_args__ = (
        Index("ix_oc_asset_id", "asset_id"),
        Index("ix_oc_status", "status"),
    )


class DbRelationshipCandidate(Base):
    """
    A suggested relationship link discovered during ingestion parsing.
    Requires Master Editor approval before being committed to the Relationship Engine.
    """
    __tablename__ = "relationship_candidates"

    id = Column(String(64), primary_key=True, default=lambda: f"rc-{uuid.uuid4().hex[:12]}")
    asset_id = Column(String(64), ForeignKey("knowledge_assets.id", ondelete="CASCADE"), nullable=False)
    source_entity_id = Column(String(128), nullable=False)   # The knowledge asset or entity
    target_entity_id = Column(String(128), nullable=True)    # Referenced entity ID (if resolved)
    target_entity_hint = Column(String(256), nullable=True)  # Raw text hint (e.g., "EAF-01")
    relationship_type = Column(String(128), nullable=False)
    confidence = Column(Float, nullable=False, default=0.0)
    status = Column(String(32), nullable=False, default="PENDING")  # PENDING|APPROVED|REJECTED
    reviewed_by = Column(String(128), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_now)

    __table_args__ = (
        Index("ix_rc_asset_id", "asset_id"),
        Index("ix_rc_status", "status"),
    )



# ─────────────────────────────────────────────
# EP-07: Workflow Engine
# ─────────────────────────────────────────────

class DbWorkflowDefinition(Base):
    """
    Stores versioned workflow definitions (states, transitions, metadata).
    """
    __tablename__ = "workflow_definitions"

    id = Column(String(128), primary_key=True, default=lambda: f"wd-{uuid.uuid4().hex[:12]}")
    name = Column(String(256), nullable=False)
    version = Column(Integer, nullable=False, default=1)
    status = Column(String(32), nullable=False, default="DRAFT") # DRAFT | PUBLISHED | ARCHIVED
    description = Column(Text, nullable=True)
    definition_payload = Column(JSONB, nullable=False) # The visual graph (states, actions, transitions)
    created_by = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), default=_now)
    updated_at = Column(DateTime(timezone=True), default=_now, onupdate=_now)

    __table_args__ = (
        UniqueConstraint('name', 'version', name='uq_workflow_name_version'),
    )

class DbWorkflowInstance(Base):
    """
    Tracks an active execution of a workflow.
    """
    __tablename__ = "workflow_instances"

    id = Column(String(128), primary_key=True, default=lambda: f"wi-{uuid.uuid4().hex[:12]}")
    workflow_id = Column(String(128), ForeignKey("workflow_definitions.id"), nullable=False)
    target_entity_id = Column(String(128), nullable=True) # ID of the object this workflow acts upon
    target_entity_type = Column(String(128), nullable=True)
    status = Column(String(32), nullable=False, default="RUNNING") # RUNNING | COMPLETED | FAILED | CANCELLED
    current_state = Column(String(128), nullable=False)
    context_data = Column(JSONB, nullable=False, default=dict) # Runtime state/variables
    started_by = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), default=_now)
    updated_at = Column(DateTime(timezone=True), default=_now, onupdate=_now)
    completed_at = Column(DateTime(timezone=True), nullable=True)

class DbWorkflowTask(Base):
    """
    Enterprise tasks generated by workflows.
    """
    __tablename__ = "workflow_tasks"

    id = Column(String(128), primary_key=True, default=lambda: f"wt-{uuid.uuid4().hex[:12]}")
    instance_id = Column(String(128), ForeignKey("workflow_instances.id"), nullable=False)
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="PENDING") # PENDING | IN_PROGRESS | COMPLETED | CANCELLED
    owner_id = Column(String(128), nullable=True)
    department_id = Column(String(128), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    priority = Column(String(32), nullable=False, default="MEDIUM")
    created_at = Column(DateTime(timezone=True), default=_now)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    completed_by = Column(String(128), nullable=True)

class DbWorkflowApproval(Base):
    """
    Tracks complex approvals (multi/sequential/parallel).
    """
    __tablename__ = "workflow_approvals"

    id = Column(String(128), primary_key=True, default=lambda: f"wa-{uuid.uuid4().hex[:12]}")
    instance_id = Column(String(128), ForeignKey("workflow_instances.id"), nullable=False)
    task_id = Column(String(128), ForeignKey("workflow_tasks.id"), nullable=True)
    status = Column(String(32), nullable=False, default="PENDING") # PENDING | APPROVED | REJECTED
    approver_id = Column(String(128), nullable=True)
    approver_department = Column(String(128), nullable=True)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_now)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

class DbWorkflowAuditLog(Base):
    """
    Immutable ledger of every workflow state transition.
    """
    __tablename__ = "workflow_audit_logs"

    id = Column(String(128), primary_key=True, default=lambda: f"wal-{uuid.uuid4().hex[:12]}")
    instance_id = Column(String(128), ForeignKey("workflow_instances.id"), nullable=False)
    action_type = Column(String(64), nullable=False) # STATE_CHANGE, TASK_CREATED, APPROVAL_GIVEN
    from_state = Column(String(128), nullable=True)
    to_state = Column(String(128), nullable=True)
    actor_id = Column(String(128), nullable=False)
    details = Column(JSONB, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=_now)
