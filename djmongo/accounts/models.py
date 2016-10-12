#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.db import models
from django.conf import settings
import datetime

PERMISSION_CHOICES = (('db-all', 'All MongoDB'),
                      ('db-write', 'Write MongoDB'),
                      ('db-read', 'Read MongoDB'),
                      ('create-other-users', 'create-other-users'),
                      ('create-any-socialgraph', 'create-any-socialgraph'),
                      ('delete-any-socialgraph', 'delete-any-socialgraph'),
                      )


class Permission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    permission_name = models.CharField(max_length=50,
                                       choices=PERMISSION_CHOICES)

    def __unicode__(self):
        return '%s has the %s permission.' % (
            self.user.email, self.permission_name)

    class Meta:
        unique_together = (("user", "permission_name"),)


class SocialGraph(models.Model):

    grantor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="grantor")
    grantee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="grantee")
    created_on = models.DateField(default=datetime.date.today)

    def __unicode__(self):
        return "%s --> %s since %s" % (self.grantor.username,
                                       self.grantee.username,
                                       self.created_on)

    class Meta:
        unique_together = (("grantor", "grantee"),)
        ordering = ('-created_on',)
        get_latest_by = "created_on"
