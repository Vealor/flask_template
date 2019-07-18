"""empty message

Revision ID: 888f81bd38c7
Revises: 1c78a9dd073b
Create Date: 2019-07-18 11:39:50.656313

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '888f81bd38c7'
down_revision = '1c78a9dd073b'
branch_labels = None
depends_on = None



def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cdm_labels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('script_labels', sa.String(length=256), nullable=False),
    sa.Column('english_labels', sa.String(length=256), nullable=False),
    sa.Column('is_calculated', sa.Boolean(), nullable=False),
    sa.Column('is_required', sa.Boolean(), nullable=False),
    sa.Column('is_unique', sa.Boolean(), nullable=False),
    sa.Column('datatype', sa.Enum('dt_boolean', 'dt_date', 'dt_datetime', 'dt_varchar', 'dt_float', 'dt_int', 'dt_blob', name='datatype'), nullable=False),
    sa.Column('regex', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('client_models', sa.Column('status', sa.Enum('active', 'inactive', 'pending', name='activity'), server_default='pending', nullable=False))
    op.drop_column('client_models', 'is_active')
    op.add_column('data_mappings', sa.Column('cdm_label_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'data_mappings', 'cdm_labels', ['cdm_label_id'], ['id'], ondelete='CASCADE')
    op.drop_column('data_mappings', 'is_unique')
    op.drop_column('data_mappings', 'regex')
    op.drop_column('data_mappings', 'cdm_label')
    op.drop_column('data_mappings', 'is_required')
    op.add_column('industry_models', sa.Column('status', sa.Enum('active', 'inactive', 'pending', name='activity'), server_default='pending', nullable=False))
    op.drop_column('industry_models', 'is_active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('industry_models', sa.Column('is_active', postgresql.ENUM('active', 'inactive', 'pending', name='activity'), server_default=sa.text("'pending'::activity"), autoincrement=False, nullable=False))
    op.drop_column('industry_models', 'status')
    op.add_column('data_mappings', sa.Column('is_required', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))
    op.add_column('data_mappings', sa.Column('cdm_label', postgresql.ENUM('potato', name='cdm_label'), autoincrement=False, nullable=False))
    op.add_column('data_mappings', sa.Column('regex', sa.VARCHAR(length=256), autoincrement=False, nullable=False))
    op.add_column('data_mappings', sa.Column('is_unique', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'data_mappings', type_='foreignkey')
    op.drop_column('data_mappings', 'cdm_label_id')
    op.add_column('client_models', sa.Column('is_active', postgresql.ENUM('active', 'inactive', 'pending', name='activity'), server_default=sa.text("'pending'::activity"), autoincrement=False, nullable=False))
    op.drop_column('client_models', 'status')
    op.drop_table('cdm_labels')
    # ### end Alembic commands ###
