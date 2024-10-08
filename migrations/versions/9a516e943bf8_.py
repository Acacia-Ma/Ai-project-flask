"""empty message

Revision ID: 9a516e943bf8
Revises: a8cf73aee6ae
Create Date: 2024-06-25 08:54:43.155693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a516e943bf8'
down_revision = 'a8cf73aee6ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('department_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('permission', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('permission')
        batch_op.drop_column('department_id')

    # ### end Alembic commands ###
