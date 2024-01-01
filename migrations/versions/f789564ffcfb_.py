"""empty message

Revision ID: f789564ffcfb
Revises: e4671785cac0
Create Date: 2023-12-29 19:11:39.301553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f789564ffcfb'
down_revision = 'e4671785cac0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('text_img', schema=None) as batch_op:
        batch_op.add_column(sa.Column('img_id', sa.String(length=200), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('text_img', schema=None) as batch_op:
        batch_op.drop_column('img_id')

    # ### end Alembic commands ###