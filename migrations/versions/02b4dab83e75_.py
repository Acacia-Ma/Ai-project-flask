"""empty message

Revision ID: 02b4dab83e75
Revises: 9a516e943bf8
Create Date: 2024-06-25 08:57:39.498717

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '02b4dab83e75'
down_revision = '9a516e943bf8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('department', schema=None) as batch_op:
        batch_op.alter_column('code',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('department', schema=None) as batch_op:
        batch_op.alter_column('code',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)

    # ### end Alembic commands ###
