"""
migrations/versions/0003_knowledge_platform.py
─────────────────────────────────────────────────────────────────
EP-05: Knowledge Ingestion Platform & RAG Foundation.

Creates:
  • knowledge_assets       — Master document/knowledge record
  • knowledge_chunks       — Document segments with pgvector embeddings
  • ingestion_jobs         — Full lifecycle tracking per document
  • ontology_candidates    — Suggested ontology mappings (Master Editor review)
  • relationship_candidates — Suggested relationship links (Master Editor review)

Enables the pgvector extension for semantic search.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── pgvector extension ────────────────────────────────────
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # ── knowledge_assets ─────────────────────────────────────
    op.create_table(
        'knowledge_assets',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('title', sa.String(512), nullable=False),
        sa.Column('asset_type', sa.String(128), nullable=False),
        sa.Column('source_filename', sa.String(512), nullable=True),
        sa.Column('source_uri', sa.String(1024), nullable=True),
        sa.Column('status', sa.String(32), nullable=False, server_default='DRAFT'),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
        sa.Column('language', sa.String(16), nullable=False, server_default='en'),
        sa.Column('entity_type_ref', sa.String(128), nullable=True),
        sa.Column('department_owner', sa.String(128), nullable=True),
        sa.Column('created_by', sa.String(128), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('archived_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('extracted_metadata', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('ontology_tags', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('acl', postgresql.JSONB, nullable=False, server_default='{}'),
    )
    op.create_index('ix_ka_status', 'knowledge_assets', ['status'])
    op.create_index('ix_ka_asset_type', 'knowledge_assets', ['asset_type'])
    op.create_index('ix_ka_department', 'knowledge_assets', ['department_owner'])
    op.create_index('ix_ka_created_by', 'knowledge_assets', ['created_by'])
    op.create_index('ix_ka_entity_type_ref', 'knowledge_assets', ['entity_type_ref'])

    # ── knowledge_chunks ─────────────────────────────────────
    op.create_table(
        'knowledge_chunks',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('asset_id', sa.String(64),
                  sa.ForeignKey('knowledge_assets.id', ondelete='CASCADE'), nullable=False),
        sa.Column('chunk_index', sa.Integer, nullable=False),
        sa.Column('chunk_strategy', sa.String(64), nullable=False, server_default='fixed'),
        sa.Column('text', sa.Text, nullable=False),
        sa.Column('char_start', sa.Integer, nullable=True),
        sa.Column('char_end', sa.Integer, nullable=True),
        sa.Column('token_count', sa.Integer, nullable=True),
        sa.Column('chunk_metadata', postgresql.JSONB, nullable=False, server_default='{}'),
        # pgvector: 768-dimensional vector column
        sa.Column('embedding', sa.Text, nullable=True),  # placeholder type; real type set below via raw SQL
        sa.Column('embedding_model', sa.String(128), nullable=True),
        sa.Column('embedding_version', sa.Integer, nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
    )
    # Alter embedding column to proper vector type now that extension is enabled
    op.execute("ALTER TABLE knowledge_chunks ALTER COLUMN embedding TYPE vector(768) USING embedding::vector")
    op.create_index('ix_kc_asset_id', 'knowledge_chunks', ['asset_id'])
    op.create_index('ix_kc_chunk_index', 'knowledge_chunks', ['asset_id', 'chunk_index'])
    # HNSW index for fast approximate nearest-neighbour search (cosine distance)
    op.execute(
        "CREATE INDEX ix_kc_embedding_hnsw ON knowledge_chunks "
        "USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64)"
    )

    # ── ingestion_jobs ────────────────────────────────────────
    op.create_table(
        'ingestion_jobs',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('asset_id', sa.String(64),
                  sa.ForeignKey('knowledge_assets.id', ondelete='SET NULL'), nullable=True),
        sa.Column('filename', sa.String(512), nullable=False),
        sa.Column('file_type', sa.String(64), nullable=False),
        sa.Column('file_size_bytes', sa.Integer, nullable=True),
        sa.Column('status', sa.String(32), nullable=False, server_default='QUEUED'),
        sa.Column('current_stage', sa.String(64), nullable=True),
        sa.Column('progress_pct', sa.Integer, nullable=False, server_default='0'),
        sa.Column('submitted_by', sa.String(128), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text, nullable=True),
        sa.Column('stage_log', postgresql.JSONB, nullable=False, server_default='[]'),
    )
    op.create_index('ix_ij_status', 'ingestion_jobs', ['status'])
    op.create_index('ix_ij_submitted_by', 'ingestion_jobs', ['submitted_by'])
    op.create_index('ix_ij_asset_id', 'ingestion_jobs', ['asset_id'])

    # ── ontology_candidates ───────────────────────────────────
    op.create_table(
        'ontology_candidates',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('asset_id', sa.String(64),
                  sa.ForeignKey('knowledge_assets.id', ondelete='CASCADE'), nullable=False),
        sa.Column('concept_id', sa.String(128), nullable=False),
        sa.Column('concept_label', sa.String(256), nullable=False),
        sa.Column('confidence', sa.Float, nullable=False, server_default='0'),
        sa.Column('source_text_snippet', sa.Text, nullable=True),
        sa.Column('status', sa.String(32), nullable=False, server_default='PENDING'),
        sa.Column('reviewed_by', sa.String(128), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
    )
    op.create_index('ix_oc_asset_id', 'ontology_candidates', ['asset_id'])
    op.create_index('ix_oc_status', 'ontology_candidates', ['status'])

    # ── relationship_candidates ───────────────────────────────
    op.create_table(
        'relationship_candidates',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('asset_id', sa.String(64),
                  sa.ForeignKey('knowledge_assets.id', ondelete='CASCADE'), nullable=False),
        sa.Column('source_entity_id', sa.String(128), nullable=False),
        sa.Column('target_entity_id', sa.String(128), nullable=True),
        sa.Column('target_entity_hint', sa.String(256), nullable=True),
        sa.Column('relationship_type', sa.String(128), nullable=False),
        sa.Column('confidence', sa.Float, nullable=False, server_default='0'),
        sa.Column('status', sa.String(32), nullable=False, server_default='PENDING'),
        sa.Column('reviewed_by', sa.String(128), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
    )
    op.create_index('ix_rc_asset_id', 'relationship_candidates', ['asset_id'])
    op.create_index('ix_rc_status', 'relationship_candidates', ['status'])


def downgrade() -> None:
    op.drop_table('relationship_candidates')
    op.drop_table('ontology_candidates')
    op.drop_table('ingestion_jobs')
    op.drop_table('knowledge_chunks')
    op.drop_table('knowledge_assets')
    op.execute("DROP EXTENSION IF EXISTS vector")
