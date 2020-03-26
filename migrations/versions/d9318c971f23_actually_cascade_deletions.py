"""Actually cascade deletions

Revision ID: d9318c971f23
Revises: 56b7980fb5cb
Create Date: 2020-03-25 14:30:19.132712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9318c971f23'
down_revision = '56b7980fb5cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('listing_user_id_fkey', 'listing', type_='foreignkey')
    op.create_foreign_key(None, 'listing', 'user', ['user_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'listing', type_='foreignkey')
    op.create_foreign_key('listing_user_id_fkey', 'listing', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###