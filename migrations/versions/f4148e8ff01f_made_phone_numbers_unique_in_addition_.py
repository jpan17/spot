"""Made phone numbers unique in addition to emails

Revision ID: f4148e8ff01f
Revises: bd7d3b005ddc
Create Date: 2020-03-21 22:45:14.308211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4148e8ff01f'
down_revision = 'bd7d3b005ddc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user', ['phone_number'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    # ### end Alembic commands ###
