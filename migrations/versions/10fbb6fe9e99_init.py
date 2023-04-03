"""init

Revision ID: 10fbb6fe9e99
Revises:
Create Date: 2023-03-24 10:50:55.995016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "10fbb6fe9e99"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "coaches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.Column("first_name", sa.String(length=64), nullable=False),
        sa.Column("last_name", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=128), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("profile_picture", sa.String(length=256), nullable=True),
        sa.Column("google_open_id", sa.String(length=128), nullable=True),
        sa.Column("about", sa.String(length=1024), nullable=False),
        sa.Column("certificate_url", sa.String(length=256), nullable=True),
        sa.Column("verification_token", sa.String(length=36), nullable=True),
        sa.Column("password_hash", sa.String(length=128), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("is_for_adults", sa.Boolean(), nullable=True),
        sa.Column("is_for_children", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_coaches_uuid"), "coaches", ["uuid"], unique=False)
    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.Column("email_from", sa.String(length=64), nullable=False),
        sa.Column("message", sa.String(length=1024), nullable=False),
        sa.Column("have_replied", sa.Boolean(), nullable=True),
        sa.Column("in_review", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "locations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=True),
        sa.Column("city", sa.String(length=64), nullable=True),
        sa.Column("street", sa.String(length=64), nullable=True),
        sa.Column("postal_code", sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.Column("text", sa.String(length=1024), nullable=False),
        sa.Column("author_id", sa.String(length=36), nullable=False),
        sa.Column("receiver_id", sa.String(length=36), nullable=False),
        sa.Column(
            "message_type",
            sa.Enum("MESSAGE", "NOTIFICATION", name="messagetypes"),
            nullable=True,
        ),
        sa.Column("is_read", sa.Boolean(), nullable=True),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "newsletter_subscriptions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column(
            "state", sa.Enum("NEW", "ACTIVE", "CANCELED", name="state"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sport_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "student_lesson_payments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "students",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.Column("first_name", sa.String(length=64), nullable=False),
        sa.Column("last_name", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=128), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("google_open_id", sa.String(length=128), nullable=True),
        sa.Column("verification_token", sa.String(length=64), nullable=True),
        sa.Column("password_hash", sa.String(length=128), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("profile_picture", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_students_uuid"), "students", ["uuid"], unique=False)
    op.create_table(
        "superusers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=128), nullable=False),
        sa.Column("password_hash", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "certificates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.Column("coach_id", sa.Integer(), nullable=True),
        sa.Column("certificate_url", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["coach_id"],
            ["coaches.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_certificates_uuid"), "certificates", ["uuid"], unique=False
    )
    op.create_table(
        "coach_schedules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=64), nullable=False),
        sa.Column("coach_id", sa.Integer(), nullable=True),
        sa.Column("location_id", sa.Integer(), nullable=True),
        sa.Column("notes", sa.String(length=256), nullable=True),
        sa.Column(
            "week_day",
            sa.Enum(
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
                name="weekday",
            ),
            nullable=True,
        ),
        sa.Column("begin", sa.DateTime(), nullable=False),
        sa.Column("end", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["coach_id"],
            ["coaches.id"],
        ),
        sa.ForeignKeyConstraint(
            ["location_id"],
            ["locations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "coaches_locations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("coach_id", sa.Integer(), nullable=True),
        sa.Column("location_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["coach_id"],
            ["coaches.id"],
        ),
        sa.ForeignKeyConstraint(
            ["location_id"],
            ["locations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "coaches_sports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.Column("coach_id", sa.Integer(), nullable=True),
        sa.Column("sport_id", sa.Integer(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["coach_id"],
            ["coaches.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sport_id"],
            ["sport_types.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "lessons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.Column("coach_id", sa.Integer(), nullable=True),
        sa.Column("location_id", sa.Integer(), nullable=True),
        sa.Column("sport_type_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["coach_id"],
            ["coaches.id"],
        ),
        sa.ForeignKeyConstraint(
            ["location_id"],
            ["locations.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sport_type_id"],
            ["sport_types.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "students_lessons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=64), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=True),
        sa.Column("lesson_id", sa.Integer(), nullable=True),
        sa.Column("student_lesson_payment_id", sa.Integer(), nullable=True),
        sa.Column("appointment_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["lesson_id"],
            ["lessons.id"],
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["students.id"],
        ),
        sa.ForeignKeyConstraint(
            ["student_lesson_payment_id"],
            ["student_lesson_payments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("students_lessons")
    op.drop_table("lessons")
    op.drop_table("coaches_sports")
    op.drop_table("coaches_locations")
    op.drop_table("coach_schedules")
    op.drop_index(op.f("ix_certificates_uuid"), table_name="certificates")
    op.drop_table("certificates")
    op.drop_table("superusers")
    op.drop_index(op.f("ix_students_uuid"), table_name="students")
    op.drop_table("students")
    op.drop_table("student_lesson_payments")
    op.drop_table("sport_types")
    op.drop_table("newsletter_subscriptions")
    op.drop_table("messages")
    op.drop_table("locations")
    op.drop_table("contacts")
    op.drop_index(op.f("ix_coaches_uuid"), table_name="coaches")
    op.drop_table("coaches")
    # ### end Alembic commands ###
