"""coach_id in student_lesson

Revision ID: 61a562b2f69c
Revises: f2f0f5e078e5
Create Date: 2023-04-06 15:09:06.548044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61a562b2f69c'
down_revision = 'f2f0f5e078e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students_lessons', sa.Column('coach_id', sa.Integer(), nullable=False))
    op.alter_column('students_lessons', 'student_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('students_lessons', 'schedule_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'students_lessons', 'coaches', ['coach_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'students_lessons', type_='foreignkey')
    op.alter_column('students_lessons', 'schedule_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('students_lessons', 'student_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('students_lessons', 'coach_id')
    # ### end Alembic commands ###