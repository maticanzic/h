# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from h import models


class DownvoteService(object):
    def __init__(self, session):
        self.session = session

    def downvoted(self, user, annotation):
        """
        Check if a given user has downvoted a given annotation.

        :param user: The user to check for a downvote.
        :type user: h.models.User

        :param annotation: The annotation to check for a downvote.
        :type annotation: h.models.Annotation

        :returns: True/False depending on the existence of a downvote.
        :rtype: bool
        """
        query = self.session.query(models.Downvote).filter_by(
            user=user, annotation=annotation
        )
        return query.count() > 0

    def all_downvoted(self, user, annotation_ids):
        """
        Check which of the given annotation IDs the given user has downvoted.

        :param user: The user to check for a downvote.
        :type user: h.models.User

        :param annotation_ids: The IDs of the annotations to check.
        :type annotation_ids: sequence of unicode

        :returns The subset of the IDs that the given user has downvoted.
        :rtype set of unicode
        """
        # SQLAlchemy doesn't behave in the way we might expect when handed an
        # `in_` condition with an empty sequence
        if not annotation_ids:
            return set()

        query = self.session.query(models.Downvote.annotation_id).filter(
            models.Downvote.annotation_id.in_(annotation_ids), models.Downvote.user == user
        )

        return set([f.annotation_id for f in query])

    def downvote(self, user, annotation):
        """
        Create an downvote for the given user and annotation.

        We enforce the uniqueness of an downvote, meaning one user can only
        downvote one annotation once. This method first checks if the annotation
        is already downvote by the user, if that is the case, then this
        is a no-op.

        :param user: The user upvoting the annotation.
        :type user: h.models.User

        :param annotation: The annotation to be downvoted.
        :type annotation: h.models.Annotation

        :returns: None
        :rtype: NoneType
        """
        if self.downvoted(user, annotation):
            return

        downvote = models.Downvote(user=user, annotation=annotation)
        self.session.add(downvote)


def downvote_service_factory(context, request):
    return DownvoteService(request.db)
