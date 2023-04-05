"""empty message

Revision ID: 2e3ffdc95079
Revises: c09fa80b2255
Create Date: 2023-04-04 18:02:19.927081

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2e3ffdc95079'
down_revision = 'c09fa80b2255'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coach_schedules', sa.Column('begin_hours', sa.Integer(), nullable=False))
    op.add_column('coach_schedules', sa.Column('begin_minutes', sa.Integer(), nullable=False))
    op.add_column('coach_schedules', sa.Column('duration', sa.Integer(), nullable=True))
    op.drop_column('coach_schedules', 'end')
    op.drop_column('coach_schedules', 'begin')
    op.drop_column('coach_schedules', 'week_day')
    op.drop_column('coach_schedules', 'notes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coach_schedules', sa.Column('notes', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.add_column('coach_schedules', sa.Column('week_day', postgresql.ENUM('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', name='weekday'), autoincrement=False, nullable=True))
    op.add_column('coach_schedules', sa.Column('begin', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('coach_schedules', sa.Column('end', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('coach_schedules', 'duration')
    op.drop_column('coach_schedules', 'begin_minutes')
    op.drop_column('coach_schedules', 'begin_hours')
    # ### end Alembic commands ###