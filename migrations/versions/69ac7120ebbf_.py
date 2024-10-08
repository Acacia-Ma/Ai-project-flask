"""empty message

Revision ID: 69ac7120ebbf
Revises: 4b82c3716667
Create Date: 2024-06-25 15:37:01.782938

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '69ac7120ebbf'
down_revision = '4b82c3716667'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('department', schema=None) as batch_op:
        batch_op.alter_column('parent_id',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('department', schema=None) as batch_op:
        batch_op.alter_column('parent_id',
               existing_type=sa.String(length=50),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)

    # ### end Alembic commands ###
