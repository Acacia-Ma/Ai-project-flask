"""empty message

Revision ID: 7d566e11f6d1
Revises: 4b0c49fba3f5
Create Date: 2023-12-19 16:03:48.143861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d566e11f6d1'
down_revision = '4b0c49fba3f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_key',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('platform', sa.String(length=40), nullable=False),
    sa.Column('value', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chat_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.String(length=200), nullable=False),
    sa.Column('user_id', sa.String(length=50), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('Content', sa.UnicodeText(), nullable=True),
    sa.Column('token', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(length=50), nullable=True),
    sa.Column('use_context', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.String(length=100), nullable=True),
    sa.Column('updated_at', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chat_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.String(length=40), nullable=False),
    sa.Column('user_id', sa.String(length=50), nullable=False),
    sa.Column('model_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chat_models',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('platform', sa.String(length=40), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('value', sa.String(length=255), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat_models')
    op.drop_table('chat_items')
    op.drop_table('chat_history')
    op.drop_table('api_key')
    # ### end Alembic commands ###
