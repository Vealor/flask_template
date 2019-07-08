"""empty message

Revision ID: 76f388fdacce
Revises: 
Create Date: 2019-07-05 17:31:34.803680

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '76f388fdacce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklisted_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('industries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('vendors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('industry_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['industry_id'], ['industries.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('industry_models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('pickle', sa.PickleType(), nullable=False),
    sa.Column('hyper_p', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('industry_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['industry_id'], ['industries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('action', sa.Enum('create', 'delete', 'modify', 'approve', name='actions'), nullable=False),
    sa.Column('affected_entity', sa.String(length=256), nullable=False),
    sa.Column('details', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('paredown_rules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_core', sa.Boolean(), nullable=False),
    sa.Column('industry_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['industry_id'], ['industries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_permissions',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('global_permissions', sa.Enum('it_admin', name='globalpermissions'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('classification_rules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_core', sa.Boolean(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('industry_id', sa.Integer(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['industry_id'], ['industries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('client_models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('pickle', sa.PickleType(), nullable=False),
    sa.Column('hyper_p', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('cliend_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cliend_id'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('industry_model_performances',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('industry_model_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['industry_model_id'], ['industry_models.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('is_approved', sa.Boolean(), nullable=False),
    sa.Column('is_archived', sa.Boolean(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('client_model_performances',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('client_model_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_model_id'], ['client_models.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('data_mappings',
    sa.Column('cdm_label', sa.Enum('potato', name='cdm_label'), nullable=False),
    sa.Column('column_name', sa.String(length=256), nullable=False),
    sa.Column('table_name', sa.String(length=256), nullable=False),
    sa.Column('is_required', sa.Boolean(), nullable=False),
    sa.Column('is_unique', sa.Boolean(), nullable=False),
    sa.Column('regex', sa.String(length=256), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('cdm_label', 'project_id')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('modified', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_required', sa.Boolean(), nullable=False),
    sa.Column('is_predicted', sa.Boolean(), nullable=False),
    sa.Column('recovery_probability', sa.Float(), nullable=True),
    sa.Column('rbc_predicted', sa.Boolean(), nullable=False),
    sa.Column('rbc_recovery_probability', sa.Float(), nullable=True),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.Column('data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('locked_user_id', sa.Integer(), nullable=True),
    sa.Column('vendor_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('client_model_id', sa.Integer(), nullable=True),
    sa.Column('industry_model_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_model_id'], ['client_models.id'], ),
    sa.ForeignKeyConstraint(['industry_model_id'], ['industry_models.id'], ),
    sa.ForeignKeyConstraint(['locked_user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_projects',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('project_permissions', sa.Enum('tax_admin', 'data_admin', 'tax_approver', name='projectpermissions'), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_projects')
    op.drop_table('transactions')
    op.drop_table('data_mappings')
    op.drop_table('client_model_performances')
    op.drop_table('projects')
    op.drop_table('industry_model_performances')
    op.drop_table('client_models')
    op.drop_table('classification_rules')
    op.drop_table('user_permissions')
    op.drop_table('paredown_rules')
    op.drop_table('logs')
    op.drop_table('industry_models')
    op.drop_table('clients')
    op.drop_table('vendors')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    op.drop_table('industries')
    op.drop_table('blacklisted_tokens')
    # ### end Alembic commands ###
