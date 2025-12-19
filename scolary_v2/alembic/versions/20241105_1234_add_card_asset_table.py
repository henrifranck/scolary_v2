"""add card_asset table"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20241105_1234'
down_revision = 'f2f2354581ee'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'card_asset',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('path', sa.String(length=512), nullable=False),
        sa.Column('uploaded_by_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['uploaded_by_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_card_asset_id'), 'card_asset', ['id'], unique=False)
    op.create_unique_constraint('uq_card_asset_path', 'card_asset', ['path'])


def downgrade():
    op.drop_constraint('uq_card_asset_path', 'card_asset', type_='unique')
    op.drop_index(op.f('ix_card_asset_id'), table_name='card_asset')
    op.drop_table('card_asset')
