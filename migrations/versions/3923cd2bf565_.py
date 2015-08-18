"""empty message

Revision ID: 3923cd2bf565
Revises: None
Create Date: 2015-08-15 22:40:54.492358

"""

# revision identifiers, used by Alembic.
revision = '3923cd2bf565'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gender',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('measurement_source',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('measurement_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('measurement_unit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('symbol', sa.String(length=10), nullable=True),
    sa.Column('suffix', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('gender_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gender_id'], ['gender.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('measurement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.Column('measurement_source_id', sa.Integer(), nullable=True),
    sa.Column('measurement_type_id', sa.Integer(), nullable=True),
    sa.Column('measurement_unit_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['measurement_source_id'], ['measurement_source.id'], ),
    sa.ForeignKeyConstraint(['measurement_type_id'], ['measurement_type.id'], ),
    sa.ForeignKeyConstraint(['measurement_unit_id'], ['measurement_unit.id'], ),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('measurement')
    op.drop_table('profile')
    op.drop_table('measurement_unit')
    op.drop_table('measurement_type')
    op.drop_table('measurement_source')
    op.drop_table('gender')
    ### end Alembic commands ###
