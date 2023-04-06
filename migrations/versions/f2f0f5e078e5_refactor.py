"""refactor

Revision ID: f2f0f5e078e5
Revises: 9a2ff4a65a89
Create Date: 2023-04-06 12:04:55.574348

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f2f0f5e078e5"
down_revision = "9a2ff4a65a89"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "coach_schedules", sa.Column("lesson_id", sa.Integer(), nullable=False)
    )
    op.add_column(
        "coach_schedules", sa.Column("reccurence", sa.Integer(), nullable=False)
    )
    op.add_column(
        "coach_schedules", sa.Column("start_datetime", sa.DateTime(), nullable=False)
    )
    op.add_column(
        "coach_schedules", sa.Column("end_datetime", sa.DateTime(), nullable=False)
    )
    op.alter_column(
        "coach_schedules", "coach_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.drop_constraint(
        "coach_schedules_location_id_fkey", "coach_schedules", type_="foreignkey"
    )
    op.create_foreign_key(None, "coach_schedules", "lessons", ["lesson_id"], ["id"])
    op.drop_column("coach_schedules", "begin_minutes")
    op.drop_column("coach_schedules", "begin_hours")
    op.drop_column("coach_schedules", "location_id")
    op.drop_column("coach_schedules", "week_day")
    op.drop_column("coach_schedules", "duration")
    op.add_column("lessons", sa.Column("title", sa.String(length=64), nullable=False))
    op.add_column("lessons", sa.Column("about", sa.String(length=512), nullable=True))
    op.add_column("lessons", sa.Column("max_people", sa.Integer(), nullable=True))
    op.add_column("lessons", sa.Column("price", sa.Integer(), nullable=True))
    op.add_column(
        "students_lessons", sa.Column("schedule_id", sa.Integer(), nullable=True)
    )
    op.add_column(
        "students_lessons", sa.Column("created_at", sa.DateTime(), nullable=False)
    )
    op.alter_column(
        "students_lessons",
        "appointment_time",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
    )
    op.drop_constraint(
        "students_lessons_lesson_id_fkey", "students_lessons", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "students_lessons", "coach_schedules", ["schedule_id"], ["id"]
    )
    op.drop_column("students_lessons", "date")
    op.drop_column("students_lessons", "lesson_id")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "students_lessons",
        sa.Column("lesson_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "students_lessons",
        sa.Column("date", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "students_lessons", type_="foreignkey")
    op.create_foreign_key(
        "students_lessons_lesson_id_fkey",
        "students_lessons",
        "lessons",
        ["lesson_id"],
        ["id"],
    )
    op.alter_column(
        "students_lessons",
        "appointment_time",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
    )
    op.drop_column("students_lessons", "created_at")
    op.drop_column("students_lessons", "schedule_id")
    op.drop_column("lessons", "price")
    op.drop_column("lessons", "max_people")
    op.drop_column("lessons", "about")
    op.drop_column("lessons", "title")
    op.add_column(
        "coach_schedules",
        sa.Column("duration", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "coach_schedules",
        sa.Column("week_day", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "coach_schedules",
        sa.Column("location_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "coach_schedules",
        sa.Column("begin_hours", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "coach_schedules",
        sa.Column("begin_minutes", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "coach_schedules", type_="foreignkey")
    op.create_foreign_key(
        "coach_schedules_location_id_fkey",
        "coach_schedules",
        "locations",
        ["location_id"],
        ["id"],
    )
    op.alter_column(
        "coach_schedules", "coach_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.drop_column("coach_schedules", "end_datetime")
    op.drop_column("coach_schedules", "start_datetime")
    op.drop_column("coach_schedules", "reccurence")
    op.drop_column("coach_schedules", "lesson_id")
    # ### end Alembic commands ###