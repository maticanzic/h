# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sqlalchemy as sa

from h.db import Base
from h.db import types

class Downvote(Base):
    """.

    Users can "downvote" annotations if they believe that the annotation is useful and should be ranked higher.
    """

    __tablename__ = "downvote"
    __table_args__ = (sa.UniqueConstraint("annotation_id", "user_id"),)

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    annotation_id = sa.Column(
        types.URLSafeUUID,
        sa.ForeignKey("annotation.id", ondelete="cascade"),
        nullable=False,
    )

    #: The annotation which has been downvoted.
    annotation = sa.orm.relationship("Annotation")

    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
        index=True,
    )

    #: The user who created the downvote.
    user = sa.orm.relationship("User")

    def __repr__(self):
        return "<downvote annotation_id=%s user_id=%s>" % (self.annotation_id, self.user_id)
