"""init migration

Revision ID: 290c5c816324
Revises: a174337dfac1
Create Date: 2023-03-02 16:06:59.266359

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '290c5c816324'
down_revision = 'a174337dfac1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coaches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=64), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('google_open_id', sa.String(), nullable=True),
    sa.Column('verification_token', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.Column('address_line_1', sa.String(length=64), nullable=True),
    sa.Column('address_line_2', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sport_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=64), nullable=False),
    sa.Column('sport_types_enum', sa.Enum('volleyball', 'box', 'tennis', 'swimming', name='sporttypes'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student_lesson_payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=64), nullable=False),
    sa.Column('status', sa.String(length=32), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=64), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('google_open_id', sa.String(), nullable=True),
    sa.Column('verification_token', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('coach_schedules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=64), nullable=False),
    sa.Column('coach_id', sa.Integer(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('week_day', sa.Enum('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', name='weekday'), nullable=True),
    sa.Column('begin', sa.DateTime(), nullable=False),
    sa.Column('end', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['coach_id'], ['coaches.id'], ),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coaches_sports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=64), nullable=False),
    sa.Column('coach_id', sa.Integer(), nullable=True),
    sa.Column('sport_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['coach_id'], ['coaches.id'], ),
    sa.ForeignKeyConstraint(['sport_id'], ['sport_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lessons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=64), nullable=False),
    sa.Column('coach_id', sa.Integer(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('sport_type_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['coach_id'], ['coaches.id'], ),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.ForeignKeyConstraint(['sport_type_id'], ['sport_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('students_lessons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=64), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.Column('student_lesson_payment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.ForeignKeyConstraint(['student_lesson_payment_id'], ['student_lesson_payments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_verified', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    sa.UniqueConstraint('username', name='users_username_key')
    )
    op.drop_table('students_lessons')
    op.drop_table('lessons')
    op.drop_table('coaches_sports')
    op.drop_table('coach_schedules')
    op.drop_table('students')
    op.drop_table('student_lesson_payments')
    op.drop_table('sport_types')
    op.drop_table('locations')
    op.drop_table('coaches')
    # ### end Alembic commands ###