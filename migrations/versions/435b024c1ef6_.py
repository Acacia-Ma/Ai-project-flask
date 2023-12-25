"""empty message

Revision ID: 435b024c1ef6
Revises: 7d566e11f6d1
Create Date: 2023-12-24 16:26:59.199450

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '435b024c1ef6'
down_revision = '7d566e11f6d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=50), nullable=False))
        batch_op.drop_column('user_id')

    with op.batch_alter_table('chat_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=50), nullable=False))
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', mysql.VARCHAR(length=50), nullable=False))
        batch_op.drop_column('username')

    with op.batch_alter_table('chat_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', mysql.VARCHAR(length=50), nullable=False))
        batch_op.drop_column('username')

    # ### end Alembic commands ###