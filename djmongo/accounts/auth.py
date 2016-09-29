#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import binascii
from django.http import HttpResponse
from django.contrib.auth.models import User, AnonymousUser


class HTTPAuthBackend(object):

    supports_object_permissions = False
    supports_anonymous_user = False

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def is_authenticated(self, request):
        auth_string = request.META.get('HTTP_AUTHORIZATION', None)
        print "here"

        if not auth_string:
            return False

        try:
            (authmeth, auth) = auth_string.split(" ", 1)

            if not authmeth.lower() == 'basic':
                return False

            auth = auth.strip().decode('base64')
            (username, password) = auth.split(':', 1)
        except (ValueError, binascii.Error):
            return False

        request.user = self.auth_func(username=username, password=password) \
            or AnonymousUser()

        return request.user not in (False, None, AnonymousUser())

    def challenge(self):
        resp = HttpResponse("Authorization Required")
        resp['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
        resp.status_code = 401
        return resp

    def __repr__(self):
        return u'<HTTPBasic: realm=%s>' % self.realm


class BasicBackend:

    supports_object_permissions = False
    supports_anonymous_user = False

    def authenticate(self, username=None, password=None):
        # print "Basic backend", username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class EmailBackend(BasicBackend):

    supports_object_permissions = False
    supports_anonymous_user = False

    def authenticate(self, username=None, password=None):

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user


class MobilePINBackend(BasicBackend):

    supports_object_permissions = False
    supports_anonymous_user = False

    def authenticate(self, username=None, password=None):
        # We have a non-email address username we should try username
        try:
            user = User.objects.get(mobile_phone_number=username)
        except User.DoesNotExist:
            return None

        if str(user.pin) == str(password):
            return user
        else:
            return None
