"""reviews

Revision ID: 6fa6c86d1c74
Revises: 6a60268bf39f
Create Date: 2023-03-30 12:28:56.674286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fa6c86d1c74'
down_revision = '6a60268bf39f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lesson_reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('student_lesson_id', sa.Integer(), nullable=True),
    sa.Column('coach_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(length=256), nullable=True),
    sa.Column('rate', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['coach_id'], ['coaches.id'], ),
    sa.ForeignKeyConstraint(['student_lesson_id'], ['students_lessons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('messages', 'author_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=True)
    op.add_column('students_lessons', sa.Column('review_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students_lessons', 'review_id')
    op.alter_column('messages', 'author_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=False)
    op.drop_table('lesson_reviews')
    # ### end Alembic commands ###