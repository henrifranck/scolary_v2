"""drop id_enrollment_fee from annual_register

Revision ID: 123456789abc
Revises: afe13d980da4
Create Date: 2025-12-25 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '123456789abc'
down_revision = 'afe13d980da4'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('annual_register') as batch_op:
        batch_op.drop_constraint('annual_register_ibfk_3', type_='foreignkey')
        batch_op.drop_column('id_enrollment_fee')


def downgrade():
    with op.batch_alter_table('annual_register') as batch_op:
        batch_op.add_column(sa.Column('id_enrollment_fee', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('annual_register_ibfk_3', 'enrollment_fee', ['id_enrollment_fee'], ['id'])
