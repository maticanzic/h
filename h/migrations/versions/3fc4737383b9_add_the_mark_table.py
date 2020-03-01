# -*- coding: utf-8 -*-
"""Add the mark table"""
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from alembic import op

from alembic import op
import sqlalchemy as sa

from h.db import types

revision = "3fc4737383b9"
down_revision = "79ebceb256aa"


def upgrade():
    op.create_table(
        "mark",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("annotation_id", types.URLSafeUUID, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["annotation_id"], ["annotation.id"], ondelete="cascade"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="cascade"),
        sa.UniqueConstraint("annotation_id", "user_id"),
    )


def downgrade():
    op.drop_table("mark")
