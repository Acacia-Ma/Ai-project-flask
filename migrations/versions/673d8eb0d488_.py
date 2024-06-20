"""empty message

Revision ID: 673d8eb0d488
Revises: a0a0a6da4510
Create Date: 2024-06-20 14:04:29.472769

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '673d8eb0d488'
down_revision = 'a0a0a6da4510'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.drop_column('username')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', mysql.VARCHAR(length=100), nullable=True))
        batch_op.add_column(sa.Column('updated_at', mysql.VARCHAR(length=100), nullable=True))
        batch_op.add_column(sa.Column('username', mysql.VARCHAR(length=50), nullable=False))

    # ### end Alembic commands ###