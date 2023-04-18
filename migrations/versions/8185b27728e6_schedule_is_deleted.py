"""schedule is_deleted

Revision ID: 8185b27728e6
Revises: 7a11657e06ae
Create Date: 2023-04-18 14:10:58.190372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8185b27728e6'
down_revision = '7a11657e06ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coach_schedules', sa.Column('is_deleted', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('coach_schedules', 'is_deleted')
    # ### end Alembic commands ###