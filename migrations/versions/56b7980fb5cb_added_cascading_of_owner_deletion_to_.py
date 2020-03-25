"""Added cascading of owner deletion to listings

Revision ID: 56b7980fb5cb
Revises: 9798d5266b07
Create Date: 2020-03-25 14:15:10.767013

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = '56b7980fb5cb'
down_revision = '9798d5266b07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_owner', sa.Boolean(), nullable=False),
    sa.Column('is_sitter', sa.Boolean(), nullable=False),
    sa.Column('full_name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('phone_number', sa.String(length=32), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('listing',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pet_name', sa.String(length=64), nullable=False),
    sa.Column('pet_type', ENUM('Dog', 'Cat', 'Rodent', 'Fish', 'Bird', 'Reptile', 'Other', name='pet_type', create_type=False), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('full_time', sa.Boolean(), nullable=False),
    sa.Column('zip_code', sa.String(length=10), nullable=False),
    sa.Column('extra_info', sa.String(length=1000), nullable=True),
    sa.Column('activities', sa.ARRAY(sa.String(length=64), dimensions=1), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('accepted_listings',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('listing_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['listing_id'], ['listing.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accepted_listings')
    op.drop_table('listing')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
