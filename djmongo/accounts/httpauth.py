#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4


import binascii
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


class NoAuthentication(object):
    """
    Authentication handler that always returns
    True, so no authentication is needed, nor
    initiated (`challenge` is missing.)
    """

    def is_authenticated(self, request):
        return True


class HttpBasicAuthentication(object):
    """
    Basic HTTP authenticate. Synopsis:

    Authentication handlers must implement two methods:
     - `is_authenticated`: Will be called when checking for
        authentication. Receives a `request` object, please
        set your `User` object on `request.user`, otherwise
        return False (or something that evaluates to False.)
     - `challenge`: In cases where `is_authenticated` returns
        False, the result of this method will be returned.
        This will usually be a `HttpResponse` object with
        some kind of challenge headers and 401 code on it.
    """

    def __init__(self, auth_func=authenticate, realm='API'):
        self.auth_func = auth_func
        self.realm = realm

    def is_authenticated(self, request):
        auth_string = request.META.get('HTTP_AUTHORIZATION', None)

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

    def authenticate(self, request):
        auth_string = request.META.get('HTTP_AUTHORIZATION', None)

        if not auth_string:
            return AnonymousUser

        try:
            (authmeth, auth) = auth_string.split(" ", 1)

            if not authmeth.lower() == 'basic':
                return AnonymousUser

            auth = auth.strip().decode('base64')
            (username, password) = auth.split(':', 1)
        except (ValueError, binascii.Error):
            return AnonymousUser

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


class HttpBasicSimple(HttpBasicAuthentication):

    def __init__(self, realm, username, password):
        User = get_user_model()
        self.user = User.objects.get(username=username)
        self.password = password

        super(HttpBasicSimple, self).__init__(auth_func=self.hash, realm=realm)

    def hash(self, username, password):
        if username == self.user.username and password == self.password:
            return self.user
