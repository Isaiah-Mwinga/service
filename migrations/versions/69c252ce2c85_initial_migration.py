"""Initial migration

Revision ID: 69c252ce2c85
Revises:
Create Date: 2025-02-02 07:54:48.369974

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "69c252ce2c85"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "customers", sa.Column("phone_number", sa.String(), nullable=True)
    )
    op.create_index(
        op.f("ix_customers_phone_number"),
        "customers",
        ["phone_number"],
        unique=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_customers_phone_number"), table_name="customers")
    op.drop_column("customers", "phone_number")
    # ### end Alembic commands ###
