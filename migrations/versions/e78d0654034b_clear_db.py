"""clear db

Revision ID: e78d0654034b
Revises: 144b579987a9
Create Date: 2020-03-24 20:53:40.393878

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e78d0654034b'
down_revision = '144b579987a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accepted_listings')
    op.drop_table('listing')
    op.drop_index('ix_user_email', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('user_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('is_owner', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_sitter', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('full_name', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('phone_number', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('phone_number', name='user_phone_number_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_user_email', 'user', ['email'], unique=True)
    op.create_table('accepted_listings',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('listing_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['listing_id'], ['listing.id'], name='accepted_listings_listing_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='accepted_listings_user_id_fkey')
    )
    op.create_table('listing',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('pet_name', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('pet_type', postgresql.ENUM('Dog', 'Cat', 'Rodent', 'Fish', 'Bird', 'Reptile', 'Other', name='pet_type'), autoincrement=False, nullable=False),
    sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('end_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('full_time', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('zip_code', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('extra_info', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('activities', postgresql.ARRAY(postgresql.ENUM('Feeding', 'Walking', 'Playing', 'Grooming', 'Bathing', 'Other', name='activities')), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='listing_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='listing_pkey')
    )
    # ### end Alembic commands ###
