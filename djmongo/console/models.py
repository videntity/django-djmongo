#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class CreateHistory(models.Model):

    database_name = models.CharField(max_length=100, unique=True)
    collection_name = models.CharField(max_length=100, unique=True)
    history = models.BooleanField(
        default=False,
        help_text=_("""Check this to create a historical collection.
                    When items are updated, the old data is saved in
                    another collection"""))

    class Meta:
        verbose_name_plural = _("Create Histories")
        unique_together = (('database_name', 'collection_name'),)

    def __str__(self):
        return "%s/%s" % (self.database_name, self.collection_name)
