"""Harden the stories table: required fields, timezone-aware timestamps, updated_at.

Revision ID: 3f2a9c1d8e47
Revises: 7b65bb46a819
Create Date: 2026-09-25 12:00:00

"""

import sqlalchemy as sa
from alembic import op

revision = "3f2a9c1d8e47"
down_revision = "7b65bb46a819"
branch_labels = None
depends_on = None

TEXT_COLUMNS = ("title", "topic", "text", "author")


def upgrade():
    stories = sa.table(
        "stories",
        *(sa.column(name) for name in TEXT_COLUMNS),
        sa.column("created_at", sa.DateTime()),
    )
    # Existing rows may contain NULLs, which the new NOT NULL constraints would reject.
    for name in TEXT_COLUMNS:
        op.execute(
            stories.update().where(stories.c[name].is_(None)).values({name: ""})
        )
    op.execute(
        stories.update()
        .where(stories.c.created_at.is_(None))
        .values(created_at=sa.func.current_timestamp())
    )

    is_postgres = op.get_bind().dialect.name == "postgresql"
    # Old timestamps were stored as naive UTC; tell Postgres so when converting.
    tz_using = {"postgresql_using": "created_at AT TIME ZONE 'UTC'"} if is_postgres else {}

    with op.batch_alter_table("stories") as batch_op:
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
        for name in ("title", "topic", "author"):
            batch_op.alter_column(name, existing_type=sa.String(255), nullable=False)
        batch_op.alter_column("text", existing_type=sa.Text(), nullable=False)
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),
            type_=sa.DateTime(timezone=True),
            nullable=False,
            **tz_using,
        )
        batch_op.create_index("ix_stories_created_at", ["created_at"])

    op.execute("UPDATE stories SET updated_at = created_at")
    with op.batch_alter_table("stories") as batch_op:
        batch_op.alter_column(
            "updated_at", existing_type=sa.DateTime(timezone=True), nullable=False
        )


def downgrade():
    is_postgres = op.get_bind().dialect.name == "postgresql"
    tz_using = {"postgresql_using": "created_at AT TIME ZONE 'UTC'"} if is_postgres else {}

    with op.batch_alter_table("stories") as batch_op:
        batch_op.drop_index("ix_stories_created_at")
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(timezone=True),
            type_=sa.DateTime(),
            nullable=True,
            **tz_using,
        )
        batch_op.alter_column("text", existing_type=sa.Text(), nullable=True)
        for name in ("title", "topic", "author"):
            batch_op.alter_column(name, existing_type=sa.String(255), nullable=True)
        batch_op.drop_column("updated_at")
