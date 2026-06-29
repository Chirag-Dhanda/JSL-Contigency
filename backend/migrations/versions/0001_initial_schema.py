"""
migrations/versions/0001_initial_schema.py
─────────────────────────────────────────────────────────────────
EP-01: Initial database schema for EKOS.

Creates all core tables:
  • entity_type_definitions
  • enterprise_entities
  • relationship_type_definitions
  • enterprise_relationships
  • users
  • roles
  • role_assignments
  • sessions
  • audit_log
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    # ── entity_type_definitions ───────────────────────────────
    op.create_table(
        'entity_type_definitions',
        sa.Column('type_id', sa.String(128), primary_key=True),
        sa.Column('display_name', sa.String(256), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('status', sa.String(32), nullable=False, server_default='Draft'),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('payload', postgresql.JSONB, nullable=False, server_default='{}'),
    )
    op.create_index('ix_etd_status', 'entity_type_definitions', ['status'])
    op.create_index('ix_etd_is_active', 'entity_type_definitions', ['is_active'])

    # ── enterprise_entities ───────────────────────────────────
    op.create_table(
        'enterprise_entities',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('name', sa.String(512), nullable=False),
        sa.Column('entity_type', sa.String(128), nullable=False),
        sa.Column('display_name', sa.String(512), nullable=False),
        sa.Column('status', sa.String(32), nullable=False, server_default='DRAFT'),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
        sa.Column('created_by', sa.String(128), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('modified_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('payload', postgresql.JSONB, nullable=False, server_default='{}'),
    )
    op.create_index('ix_ee_entity_type', 'enterprise_entities', ['entity_type'])
    op.create_index('ix_ee_status', 'enterprise_entities', ['status'])
    op.create_index('ix_ee_created_by', 'enterprise_entities', ['created_by'])
    op.create_index('ix_ee_name', 'enterprise_entities', ['name'])
    op.create_index('ix_ee_display_name', 'enterprise_entities', ['display_name'])
    # GIN index for JSONB containment / key-exists queries
    op.create_index('ix_ee_payload_gin', 'enterprise_entities', ['payload'],
                    postgresql_using='gin')

    # ── relationship_type_definitions ─────────────────────────
    op.create_table(
        'relationship_type_definitions',
        sa.Column('type_id', sa.String(128), primary_key=True),
        sa.Column('display_name', sa.String(256), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('is_directed', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('payload', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
    )

    # ── enterprise_relationships ──────────────────────────────
    op.create_table(
        'enterprise_relationships',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('source_entity_id', sa.String(64), nullable=False),
        sa.Column('target_entity_id', sa.String(64), nullable=False),
        sa.Column('relationship_type', sa.String(128), nullable=False),
        sa.Column('direction', sa.String(32), nullable=False, server_default='DIRECTED'),
        sa.Column('created_by', sa.String(128), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('rel_metadata', postgresql.JSONB, nullable=False, server_default='{}'),
    )
    op.create_index('ix_er_source', 'enterprise_relationships', ['source_entity_id'])
    op.create_index('ix_er_target', 'enterprise_relationships', ['target_entity_id'])
    op.create_index('ix_er_type', 'enterprise_relationships', ['relationship_type'])
    op.create_index('ix_er_source_type', 'enterprise_relationships',
                    ['source_entity_id', 'relationship_type'])

    # ── users ─────────────────────────────────────────────────
    op.create_table(
        'users',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('email', sa.String(256), nullable=False, unique=True),
        sa.Column('username', sa.String(128), nullable=False, unique=True),
        sa.Column('full_name', sa.String(256), nullable=True),
        sa.Column('hashed_password', sa.String(256), nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('is_verified', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('department_id', sa.String(64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_username', 'users', ['username'])

    # ── roles ─────────────────────────────────────────────────
    op.create_table(
        'roles',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('name', sa.String(64), nullable=False, unique=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('permissions', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('is_system_role', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
    )

    # Seed system roles
    op.execute("""
        INSERT INTO roles (id, name, description, permissions, is_system_role) VALUES
        ('role-sysadmin', 'PLATFORM_ADMIN',   'Full platform administration',           '["*"]',  true),
        ('role-meditor',  'MASTER_EDITOR',    'Can approve/publish all knowledge',      '["knowledge.*","metadata.*","workflow.approve"]', true),
        ('role-ceditor',  'CONTENT_EDITOR',   'Can create/edit draft knowledge',        '["knowledge.create","metadata.create","metadata.update"]', true),
        ('role-depthead', 'DEPARTMENT_HEAD',  'Department-scoped management',           '["knowledge.read","metadata.read","reporting.*"]', true),
        ('role-viewer',   'VIEWER',           'Read-only access across the platform',   '["*.read"]', true)
    """)

    # ── role_assignments ──────────────────────────────────────
    op.create_table(
        'role_assignments',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('user_id', sa.String(64),
                  sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role_id', sa.String(64),
                  sa.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('assigned_by', sa.String(64), nullable=True),
        sa.Column('assigned_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.UniqueConstraint('user_id', 'role_id', name='uq_user_role'),
    )
    op.create_index('ix_ra_user_id', 'role_assignments', ['user_id'])

    # ── sessions ──────────────────────────────────────────────
    op.create_table(
        'sessions',
        sa.Column('jti', sa.String(128), primary_key=True),
        sa.Column('user_id', sa.String(64), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_sessions_user_id', 'sessions', ['user_id'])
    op.create_index('ix_sessions_revoked', 'sessions', ['revoked'])

    # ── audit_log ─────────────────────────────────────────────
    op.create_table(
        'audit_log',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('user_id', sa.String(128), nullable=False),
        sa.Column('entity_id', sa.String(128), nullable=True),
        sa.Column('module', sa.String(128), nullable=False),
        sa.Column('action', sa.String(128), nullable=False),
        sa.Column('old_value', postgresql.JSONB, nullable=True),
        sa.Column('new_value', postgresql.JSONB, nullable=True),
        sa.Column('reason', sa.Text, nullable=True),
        sa.Column('ip_address', sa.String(64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
    )
    op.create_index('ix_audit_entity_id', 'audit_log', ['entity_id'])
    op.create_index('ix_audit_user_id', 'audit_log', ['user_id'])
    op.create_index('ix_audit_action', 'audit_log', ['action'])
    op.create_index('ix_audit_created_at', 'audit_log', ['created_at'])


def downgrade() -> None:
    op.drop_table('audit_log')
    op.drop_table('sessions')
    op.drop_table('role_assignments')
    op.drop_table('roles')
    op.drop_table('users')
    op.drop_table('enterprise_relationships')
    op.drop_table('relationship_type_definitions')
    op.drop_table('enterprise_entities')
    op.drop_table('entity_type_definitions')
