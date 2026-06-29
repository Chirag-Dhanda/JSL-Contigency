"""
migrations/versions/0002_entity_type_versions.py
─────────────────────────────────────────────────────────────────
EP-02: Add entity_type_versions table.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'entity_type_versions',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('type_id', sa.String(128),
                  sa.ForeignKey('entity_type_definitions.type_id', ondelete='CASCADE'),
                  nullable=False),
        sa.Column('version', sa.Integer, nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('payload', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('created_by', sa.String(128), nullable=False, server_default='system'),
        sa.UniqueConstraint('type_id', 'version', name='uq_type_version')
    )
    op.create_index('ix_etv_type_id', 'entity_type_versions', ['type_id'])

def downgrade() -> None:
    op.drop_table('entity_type_versions')
