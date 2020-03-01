# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from zope.interface import implementer

from h.formatters.interfaces import IAnnotationFormatter


@implementer(IAnnotationFormatter)
class AnnotationUpvoteFormatter(object):
    """
    Formatter for exposing a user's annotation upvotes.

    If the passed-in user has upvoted an annotation, this formatter will
    add: `"upvoted": true` to the payload, otherwise `"upvoted": false`.
    """

    def __init__(self, upvote_service, user=None):
        self.upvote_service = upvote_service
        self.user = user

        # Local cache of upvotes. We don't need to care about detached
        # instances because we only store the annotation id and a boolean upvote.
        self._cache = {}

    def preload(self, ids):
        if self.user is None:
            return

        upvoted_ids = self.upvote_service.all_upvoted(user=self.user, annotation_ids=ids)

        upovotes = {id_: (id_ in upvoted_ids) for id_ in ids}
        self._cache.update(upvotes)
        return upvotes

    def format(self, annotation_resource):
        upvoted = self._load(annotation_resource.annotation)
        return {"upvoted": upvoted}

    def _load(self, annotation):
        if self.user is None:
            return False

        id_ = annotation.id

        if id_ in self._cache:
            return self._cache[id_]

        upvoted = self.upvote_service.upvoted(user=self.user, annotation=annotation)
        self._cache[id_] = upvoted
        return self._cache[id_]
