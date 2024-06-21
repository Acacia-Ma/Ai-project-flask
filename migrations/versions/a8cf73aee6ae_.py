"""empty message

Revision ID: a8cf73aee6ae
Revises: 790b40145372
Create Date: 2024-06-21 16:43:08.387518

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a8cf73aee6ae'
down_revision = '790b40145372'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_items', schema=None) as batch_op:
        batch_op.alter_column('model_id',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=40),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_items', schema=None) as batch_op:
        batch_op.alter_column('model_id',
               existing_type=sa.String(length=40),
               type_=mysql.INTEGER(display_width=11),
               nullable=True)

    # ### end Alembic commands ###
