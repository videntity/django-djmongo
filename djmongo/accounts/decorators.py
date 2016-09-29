#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4


"""
    Decorator to check for credentials before responding on json requests.
"""

from functools import update_wrapper, wraps
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .utils import unauthorized_json_response, user_permissions


def json_login_required(func):
    """
        Put this decorator before your view to check if the user is logged in
        and return a JSON 401 error if he/she is not.
    """

    def wrapper(request, *args, **kwargs):
        user = None
        # get the Basic username and password from the request.
        auth_string = request.META.get('HTTP_AUTHORIZATION', None)

        if auth_string:
            (authmeth, auth) = auth_string.split(" ", 1)
            auth = auth.strip().decode('base64')
            (username, password) = auth.split(':', 1)

            # print username, password
            user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            return HttpResponse(unauthorized_json_response(), status=401,
                                content_type="application/json")
        login(request, user)
        return func(request, *args, **kwargs)

    return update_wrapper(wrapper, func)


def access_required(permission):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            if permission in user_permissions(request):
                return func(request, *args, **kwargs)
            else:
                return HttpResponse(unauthorized_json_response(), status=401,
                                    content_type="application/json")
        return wraps(func)(inner_decorator)

    return decorator
