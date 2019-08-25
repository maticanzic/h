# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from h import models


class UpvoteService(object):
    def __init__(self, session):
        self.session = session

    def upvoted(self, user, annotation):
        """
        Check if a given user has upvoted a given annotation.

        :param user: The user to check for a upvote.
        :type user: h.models.User

        :param annotation: The annotation to check for a upvote.
        :type annotation: h.models.Annotation

        :returns: True/False depending on the existence of a upvote.
        :rtype: bool
        """
        query = self.session.query(models.Upvote).filter_by(
            user=user, annotation=annotation
        )
        return query.count() > 0

    def all_upvoted(self, user, annotation_ids):
        """
        Check which of the given annotation IDs the given user has upvoted.

        :param user: The user to check for an upvote.
        :type user: h.models.User

        :param annotation_ids: The IDs of the annotations to check.
        :type annotation_ids: sequence of unicode

        :returns The subset of the IDs that the given user has upvoted.
        :rtype set of unicode
        """
        # SQLAlchemy doesn't behave in the way we might expect when handed an
        # `in_` condition with an empty sequence
        if not annotation_ids:
            return set()

        query = self.session.query(models.Upvote.annotation_id).filter(
            models.Upvote.annotation_id.in_(annotation_ids), models.Upvote.user == user
        )

        return set([f.annotation_id for f in query])

    def upvote(self, user, annotation):
        """
        Create an upvote for the given user and annotation.

        We enforce the uniqueness of an upvote, meaning one user can only
        upvote one annotation once. This method first checks if the annotation
        is already upvoted by the user, if that is the case, then this
        is a no-op.

        :param user: The user upvoting the annotation.
        :type user: h.models.User

        :param annotation: The annotation to be upvoted.
        :type annotation: h.models.Annotation

        :returns: None
        :rtype: NoneType
        """
        if self.upvoted(user, annotation):
            return

        upvote = models.Upvote(user=user, annotation=annotation)
        self.session.add(upvote)


def upvote_service_factory(context, request):
    return UpvoteService(request.db)
