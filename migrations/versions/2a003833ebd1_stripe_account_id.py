"""stripe account_id

Revision ID: 2a003833ebd1
Revises: d61815b6d34a
Create Date: 2023-04-12 12:52:14.328715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2a003833ebd1"
down_revision = "d61815b6d34a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "coaches", sa.Column("stripe_account_id", sa.String(length=32), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("coaches", "stripe_account_id")
    # ### end Alembic commands ###
