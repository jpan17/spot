"""empty message

Revision ID: 09cd6c44ce2c
Revises: f4148e8ff01f
Create Date: 2020-03-24 20:16:28.992086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09cd6c44ce2c'
down_revision = 'f4148e8ff01f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('listing', sa.Column('temp', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('listing', 'temp')
    # ### end Alembic commands ###
