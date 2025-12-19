"""add file_asset table"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20241110_0001'
down_revision = '20241105_1234'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'file_asset',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('path', sa.String(length=512), nullable=False),
        sa.Column('type', sa.Enum('image', 'video', 'audio', 'document', 'other', name='filetypeenum'), nullable=False, server_default='other'),
        sa.Column('size_bytes', sa.BigInteger(), nullable=True),
        sa.Column('mime_type', sa.String(length=255), nullable=True),
        sa.Column('uploaded_by_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['uploaded_by_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('path', name='uq_file_asset_path')
    )
    op.create_index(op.f('ix_file_asset_id'), 'file_asset', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_file_asset_id'), table_name='file_asset')
    op.drop_table('file_asset')
