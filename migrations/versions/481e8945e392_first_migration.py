"""first migration

Revision ID: 481e8945e392
Revises: 
Create Date: 2021-06-10 20:48:19.617258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '481e8945e392'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=False),
    sa.Column('last_name', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('phone_no', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=20), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_company_name'), 'users', ['company_name'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_last_name'), 'users', ['last_name'], unique=False)
    op.create_index(op.f('ix_users_phone_no'), 'users', ['phone_no'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('project_name', sa.String(length=30), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('upload_name', sa.String(length=30), nullable=False),
    sa.Column('video_name', sa.String(length=30), nullable=False),
    sa.Column('video_format', sa.String(length=5), nullable=False),
    sa.Column('video_size', sa.String(length=5), nullable=False),
    sa.Column('select_gpu', sa.String(length=4), nullable=False),
    sa.Column('compute_hrs', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_compute_hrs'), 'projects', ['compute_hrs'], unique=False)
    op.create_index(op.f('ix_projects_description'), 'projects', ['description'], unique=False)
    op.create_index(op.f('ix_projects_project_name'), 'projects', ['project_name'], unique=False)
    op.create_index(op.f('ix_projects_select_gpu'), 'projects', ['select_gpu'], unique=False)
    op.create_index(op.f('ix_projects_upload_name'), 'projects', ['upload_name'], unique=False)
    op.create_index(op.f('ix_projects_user_id'), 'projects', ['user_id'], unique=False)
    op.create_index(op.f('ix_projects_video_format'), 'projects', ['video_format'], unique=False)
    op.create_index(op.f('ix_projects_video_name'), 'projects', ['video_name'], unique=False)
    op.create_index(op.f('ix_projects_video_size'), 'projects', ['video_size'], unique=False)
    op.create_table('jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('current_project_id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.String(length=30), nullable=False),
    sa.Column('status', sa.String(length=15), nullable=False),
    sa.ForeignKeyConstraint(['current_project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_jobs_current_project_id'), 'jobs', ['current_project_id'], unique=False)
    op.create_index(op.f('ix_jobs_job_id'), 'jobs', ['job_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_jobs_job_id'), table_name='jobs')
    op.drop_index(op.f('ix_jobs_current_project_id'), table_name='jobs')
    op.drop_table('jobs')
    op.drop_index(op.f('ix_projects_video_size'), table_name='projects')
    op.drop_index(op.f('ix_projects_video_name'), table_name='projects')
    op.drop_index(op.f('ix_projects_video_format'), table_name='projects')
    op.drop_index(op.f('ix_projects_user_id'), table_name='projects')
    op.drop_index(op.f('ix_projects_upload_name'), table_name='projects')
    op.drop_index(op.f('ix_projects_select_gpu'), table_name='projects')
    op.drop_index(op.f('ix_projects_project_name'), table_name='projects')
    op.drop_index(op.f('ix_projects_description'), table_name='projects')
    op.drop_index(op.f('ix_projects_compute_hrs'), table_name='projects')
    op.drop_table('projects')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_phone_no'), table_name='users')
    op.drop_index(op.f('ix_users_last_name'), table_name='users')
    op.drop_index(op.f('ix_users_first_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_company_name'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
