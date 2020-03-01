# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from h import models


class MarkService(object):
    def __init__(self, session):
        self.session = session

    def marked(self, user, annotation):
        """
        Check if a given user has marked a given annotation.

        :param user: The user to check for a mark.
        :type user: h.models.User

        :param annotation: The annotation to check for a mark.
        :type annotation: h.models.Annotation

        :returns: True/False depending on the existence of a mark.
        :rtype: bool
        """
        query = self.session.query(models.Mark).filter_by(
            user=user, annotation=annotation
        )
        return query.count() > 0

    def all_marked(self, user, annotation_ids):
        """
        Check which of the given annotation IDs the given user has marked.

        :param user: The user to check for a mark.
        :type user: h.models.User

        :param annotation_ids: The IDs of the annotations to check.
        :type annotation_ids: sequence of unicode

        :returns The subset of the IDs that the given user has marked.
        :rtype set of unicode
        """
        # SQLAlchemy doesn't behave in the way we might expect when handed an
        # `in_` condition with an empty sequence
        if not annotation_ids:
            return set()

        query = self.session.query(models.Mark.annotation_id).filter(
            models.Mark.annotation_id.in_(annotation_ids), models.Mark.user == user
        )

        return set([f.annotation_id for f in query])

    def mark(self, user, annotation):
        """
        Create a mark for the given user and annotation.

        We enforce the uniqueness of the mark, meaning one user (admin) can only
        mark one annotation once. This method first checks if the annotation
        is already marked by the admin, if that is the case, then this
        is a no-op.

        :param user: The user marking the annotation.
        :type user: h.models.User

        :param annotation: The annotation to be marked.
        :type annotation: h.models.Annotation

        :returns: None
        :rtype: NoneType
        """
        if self.marked(user, annotation):
            return

        mark = models.Mark(user=user, annotation=annotation)
        self.session.add(mark)


def mark_service_factory(context, request):
    return MarkService(request.db)
