# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from zope.interface import implementer

from h.formatters.interfaces import IAnnotationFormatter


@implementer(IAnnotationFormatter)
class AnnotationDownvoteFormatter(object):
    """
    Formatter for exposing a user's annotation downvotes.

    If the passed-in user has downvoted an annotation, this formatter will
    add: `"downvoted": true` to the payload, otherwise `"downvoted": false`.
    """

    def __init__(self, downvote_service, user=None):
        self.downvote_service = downvote_service
        self.user = user

        # Local cache of downvotes. We don't need to care about detached
        # instances because we only store the annotation id and a boolean downvote.
        self._cache = {}

    def preload(self, ids):
        if self.user is None:
            return

        downvoted_ids = self.downvote_service.all_downvoted(user=self.user, annotation_ids=ids)

        upovotes = {id_: (id_ in downvoted_ids) for id_ in ids}
        self._cache.update(downvotes)
        return downvotes

    def format(self, annotation_resource):
        downvoted = self._load(annotation_resource.annotation)
        return {"downvoted": downvoted}

    def _load(self, annotation):
        if self.user is None:
            return False

        id_ = annotation.id

        if id_ in self._cache:
            return self._cache[id_]

        downvoted = self.downvote_service.downvoted(user=self.user, annotation=annotation)
        self._cache[id_] = downvoted
        return self._cache[id_]
