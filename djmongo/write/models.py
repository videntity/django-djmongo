#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
import json
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from collections import OrderedDict
from django.contrib.auth import get_user_model



class WriteAPIHTTPAuth(models.Model):
    created_by = models.ForeignKey(
        get_user_model(), blank=True, null=True, on_delete=models.CASCADE)
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

    http_post = models.BooleanField(default=True, blank=True)
    http_put = models.BooleanField(default=True, blank=True)
    database_name = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    json_schema = models.TextField(
        max_length=20480,
        default="{}",
        verbose_name="JSON Schema",
        help_text="""Default "{}", means no JSON Schema.""")
    readme_md = models.TextField(max_length=4096, default="", blank=True)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = _("Write APIs with HTTPAuth")
        verbose_name = _("Write API with HTTPAuth")

    def url(self):
        return reverse('djmongo_api_write_to_collection_with_httpauth', args=(self.slug,))

    def __str__(self):
        return "%s" % (self.slug)

    def allgroups(self):
        groups = []
        for g in self.groups.all():
            groups.append(g.name)
        return json.dumps(groups)

    def http_methods(self):
        l = []
        if self.http_post:
            l.append("POST")
        if self.http_put:
            l.append("PUT")
        return l

    def auth_method(self):
        return 'httpauth'

    def http_get_response(self):
        od = OrderedDict()
        od['http_methods'] = self.http_methods()
        od['auth_method'] = self.auth_method()
        od['json_schema'] = self.json_schema
        od['readme'] = self.readme_md
        return od



class WriteAPIIP(models.Model):
    created_by = models.ForeignKey(
        get_user_model(), blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    http_post = models.BooleanField(default=True, blank=True)
    http_put = models.BooleanField(default=True, blank=True)
    database_name = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    json_schema = models.TextField(
        max_length=20480,
        default="{}",
        verbose_name="JSON Schema",
        help_text="""Default "{}", means no JSON Schema.""")
    from_ip = models.TextField(max_length=2048, default="127.0.0.1",
                               verbose_name=_("From IPs"),
                               help_text=_("Only accept requests from a IP in "
                                           "this list separated by whitespace "
                                           ". 0.0.0.0 means all."))
    readme_md = models.TextField(max_length=4096, default="", blank=True)
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

    def url(self):
        return reverse('djmongo_api_write_to_collection_with_ip', args=(self.slug,))

    def http_methods(self):
        l = []
        if self.http_post:
            l.append("POST")
        if self.http_put:
            l.append("PUT")
        return l

    def auth_method(self):
        return 'ip'

    def http_get_response(self):
        od = OrderedDict()
        od['http_methods'] = self.http_methods()
        od['auth_method'] = self.auth_method()
        od['json_schema'] = self.json_schema
        od['readme'] = self.readme_md
        return od



class WriteAPIOAuth2(models.Model):

    created_by = models.ForeignKey(
        get_user_model(), blank=True, null=True, on_delete=models.CASCADE)
    scopes = models.CharField(max_length=1024, default="*", blank=True,
                              help_text="Space delimited list of scopes required. * means no scope is required.")
    http_post = models.BooleanField(default=True, blank=True)
    http_put = models.BooleanField(default=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    database_name = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    json_schema = models.TextField(
        max_length=20480,
        default="{}",
        verbose_name="JSON Schema",
        help_text="""Default "{}", means no JSON Schema.""")
    readme_md = models.TextField(max_length=4096, default="", blank=True)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = "Write APIs with OAuth2 Auth"
        verbose_name = "Write API with OAuth2 Auth"

    def __str__(self):
        return "%s" % (self.slug)

    def http_methods(self):
        l = []
        if self.http_post:
            l.append("POST")
        if self.http_put:
            l.append("PUT")
        return l

    def auth_method(self):
        return 'oauth2'

    def http_get_response(self):
        od = OrderedDict()
        od['http_methods'] = self.http_methods()
        od['auth_method'] = self.auth_method()
        od['json_schema'] = self.json_schema
        od['readme'] = self.readme_md
        return od
