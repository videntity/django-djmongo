#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
import json
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse


@python_2_unicode_compatible
class WriteAPIHTTPAuth(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="djmongo_write_httpauth_groups",
        help_text=_(
            "Use ctrl to select multiple "
            "groups. If no groups are "
            "selected blank, any user may "
            "access the API."))
    slug = models.SlugField(max_length=100, unique=True, help_text=_(
        "The slug is the unique part of the URL for your API."))
    database_name = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    json_schema = models.TextField(
        max_length=2048,
        default="{}",
        verbose_name="JSON Schema",
        help_text="""Default "{}", means no JSON Schema.""")
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = _("Write APIs with HTTPAuth")
        verbose_name = _("Write API with HTTPAuth")

    def url(self):
        return reverse('write_to_collection_httpauth', args=(self.slug,))

    def __str__(self):
        return "%s" % (self.slug)

    def allgroups(self):
        groups = []
        for g in self.groups.all():
            groups.append(g.name)
        return json.dumps(groups)


@python_2_unicode_compatible
class WriteAPIIP(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    database_name = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    json_schema = models.TextField(
        max_length=2048,
        default="{}",
        verbose_name="JSON Schema",
        help_text="""Default "{}", means no JSON Schema.""")
    from_ip = models.TextField(max_length=2048, default="127.0.0.1",
                               verbose_name=_("From IPs"),
                               help_text=_("Only accept requests from a IP in "
                                           "this list separated by whitespace "
                                           ". 0.0.0.0 means all."))
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = _("Write APIs with IP Address Auth")
        verbose_name = _("Write API with IP Address Auth")

    def allowable_ips(self):
        allowable_ips = self.from_ip.split(" ")
        return allowable_ips

    def __str__(self):
        return "%s" % (self.slug)


@python_2_unicode_compatible
class WriteAPIoAuth2(models.Model):

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True,
                                    related_name="djmongo_write_oauth_groups")
    slug = models.SlugField(max_length=100, unique=True)
    database_name = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    json_schema = models.TextField(
        max_length=2048,
        default="{}",
        verbose_name="JSON Schema",
        help_text="""Default "{}", means no JSON Schema.""")
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = "Write APIs with oAuth2 Auth"
        verbose_name = "Write API with oAuth2 Auth"

    def __str__(self):
        return "%s" % (self.slug)
