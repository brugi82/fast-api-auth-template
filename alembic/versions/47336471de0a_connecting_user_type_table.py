"""Connecting user type table

Revision ID: 47336471de0a
Revises: 34b07fea0921
Create Date: 2022-09-20 16:43:44.974754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "47336471de0a"
down_revision = "34b07fea0921"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    user_type_table = op.create_table(
        "user_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "name",
            sa.Enum("Admin", "Regular", "Anonimous", name="usertype"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_types_id"), "user_types", ["id"], unique=False)
    op.add_column("confirmations", sa.Column("issued_at", sa.DateTime(), nullable=True))
    op.add_column("users", sa.Column("user_type_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "users", "user_types", ["user_type_id"], ["id"])
    # ### end Alembic commands ###
    op.bulk_insert(
        user_type_table,
        [
            {id: 0, name: "Admin"},
            {id: 1, name: "Regular"},
            {id: 2, name: "Anonimous"},
        ],
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="foreignkey")
    op.drop_column("users", "user_type_id")
    op.drop_column("confirmations", "issued_at")
    op.drop_index(op.f("ix_user_types_id"), table_name="user_types")
    op.drop_table("user_types")
    # ### end Alembic commands ###
