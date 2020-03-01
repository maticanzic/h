# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from zope.interface import implementer

from h.formatters.interfaces import IAnnotationFormatter


@implementer(IAnnotationFormatter)
class AnnotationMarkFormatter(object):
    """
    Formatter for exposing admin's annotation marks.

    If the passed-in user has marked an annotation, this formatter will
    add: `"markedByAdmin": true` to the payload, otherwise `"markedByAdmin": false`.
    """

    def __init__(self, mark_service, user=None):
        self.mark_service = mark_service
        self.user = user

        # Local cache of marked annotations. We don't need to care about detached
        # instances because we only store the annotation id and a boolean markedByAdmin.
        self._cache = {}

    def preload(self, ids):
        if self.user is None:
            return

        marked_ids = self.mark_service.all_marked(user=self.user, annotation_ids=ids)

        marks = {id_: (id_ in marked_ids) for id_ in ids}
        self._cache.update(marks)
        return marks

    def format(self, annotation_resource):
        markedByAdmin = self._load(annotation_resource.annotation)
        return {"markedByAdmin": markedByAdmin}

    def _load(self, annotation):
        if self.user is None:
            return False

        id_ = annotation.id

        if id_ in self._cache:
            return self._cache[id_]

        markedByAdmin = self.mark_service.marked(user=self.user, annotation=annotation)
        self._cache[id_] = markedByAdmin
        return self._cache[id_]
