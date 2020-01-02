#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4


"""
    Decorator to check for credentials before responding on API requests.
    Response with JSON instead of standard login redirect.
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf import settings
import base64
from collections import OrderedDict
from functools import update_wrapper
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .utils import unauthorized_json_response
from .read.models import HTTPAuthReadAPI, PublicReadAPI, IPAuthReadAPI, CustomIPAuthReadAPI
from .write.models import WriteAPIIP
import shlex
import json


def httpauth_login_required(func):
    """
        Put this decorator before your view to check if the user is logged in
        via httpauth and return a JSON 401 error if he/she is not.
    """

    def wrapper(request, *args, **kwargs):
        user = None
        # get the Basic username and password from the request.
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    username, password = base64.b64decode(
                        auth[1]).decode('utf-8').split(':')
                    # print(username, password)
                    user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            return HttpResponse(unauthorized_json_response(),
                                content_type="application/json", status=401)
        login(request, user)
        return func(request, *args, **kwargs)

    return update_wrapper(wrapper, func)


def ip_write_verification_required(func):
    """
        Put this decorator before your view to check if the function is coming from an IP on file
    """

    def wrapper(request, *args, **kwargs):

        slug = kwargs.get('slug', "")
        if not slug:
            return kickout_404("Not found.", content_type="application/json")

        try:
            wip = WriteAPIIP.objects.get(slug=slug)
            ip = get_client_ip(request)
            if ip not in wip.allowable_ips() and "0.0.0.0" not in wip.allowable_ips():
                msg = "The IP %s is not authorized to make the API call." % (
                    ip)
                return kickout_401(msg)

        except WriteAPIIP.DoesNotExist:
            return HttpResponse(unauthorized_json_response(),
                                content_type="application/json")

        return func(request, *args, **kwargs)

    return update_wrapper(wrapper, func)


def ipauth_read_verification_required(func):
    """
        Put this decorator before your view to check if the function is coming from an IP on file
    """

    def wrapper(request, *args, **kwargs):

        slug = kwargs.get('slug', "")
        database_name = kwargs.get('database_name', "")
        collection_name = kwargs.get('collection_name', "")
        if not slug:
            return kickout_404("Not found.", content_type="application/json")

        try:
            rip = IPAuthReadAPI.objects.get(slug=slug, database_name=database_name,
                                            collection_name=collection_name)
            ip = get_client_ip(request)
            if ip not in rip.allowable_ips() and "0.0.0.0" not in rip.allowable_ips():
                msg = "The IP %s is not authorized to make the API call." % (
                    ip)
                return kickout_401(msg)

        except IPAuthReadAPI.DoesNotExist:
            return HttpResponse(unauthorized_json_response(),
                                content_type="application/json")

        return func(request, *args, **kwargs)

    return update_wrapper(wrapper, func)


def custom_ipauth_read_verification_required(func):
    """
        Put this decorator before your view to check if the function is coming from an IP on file
    """

    def wrapper(request, *args, **kwargs):

        slug = kwargs.get('slug', "")
        if not slug:
            return kickout_404("Not found.", content_type="application/json")

        try:
            rip = CustomIPAuthReadAPI.objects.get(slug=slug)
            ip = get_client_ip(request)
            if ip not in rip.allowable_ips() and "0.0.0.0" not in rip.allowable_ips():
                msg = "The IP %s is not authorized to make the API call." % (
                    ip)
                return kickout_401(msg)

        except CustomIPAuthReadAPI.DoesNotExist:
            return HttpResponse(unauthorized_json_response(),
                                content_type="application/json")

        return func(request, *args, **kwargs)

    return update_wrapper(wrapper, func)


def check_public_ok(func):
    """
        Call after login decorator.
    """

    def wrapper(request, *args, **kwargs):
        default_to_open = getattr(settings, 'DEFAULT_TO_OPEN_READ', False)
        database_name = kwargs.get('database_name', "")
        collection_name = kwargs.get('collection_name', "")
        slug = kwargs.get('slug', "")
        if not default_to_open:
            if not database_name or not collection_name:
                return HttpResponse(unauthorized_json_response(),
                                    content_type="application/json")
            try:
                pub_read_api = PublicReadAPI.objects.get(slug=slug,
                                                         database_name=database_name,
                                                         collection_name=collection_name)
            except PublicReadAPI.DoesNotExist:
                return HttpResponse(unauthorized_json_response(),
                                    content_type="application/json")

            # If search keys have been limited...
            if pub_read_api.search_keys:
                search_key_list = shlex.split(pub_read_api.search_keys)
                for k in request.GET.keys():

                    if k not in search_key_list:
                        message = "Search key %s is not allowed." % (k)

                        body = {"code": 400,
                                "message": k,
                                "errors": [message, ]}

                        return HttpResponse(json.dumps(body, indent=4, ),
                                            content_type="application/json")
        return func(request, *args, **kwargs)

    return update_wrapper(wrapper, func)


def check_read_httpauth_access(func):
    """
        Call after login decorator.
    """

    def wrapper(request, *args, **kwargs):
        database_name = kwargs.get('database_name', "")
        collection_name = kwargs.get('collection_name', "")
        slug = kwargs.get('slug', "")
        if not database_name or not collection_name:
            return HttpResponse(unauthorized_json_response(),
                                content_type="application/json")

        try:
            # Check to see if we have a matching record in DB access.
            dac = HTTPAuthReadAPI.objects.get(slug=slug,
                                              database_name=database_name,
                                              collection_name=collection_name)
        except HTTPAuthReadAPI.DoesNotExist:
            return HttpResponse(unauthorized_json_response(),
                                content_type="application/json")

        dac_groups = dac.groups.all()
        user_groups = request.user.groups.all()

        # allowed groups
        in_group = False
        for dg in dac_groups:
            if dg in user_groups:
                in_group = True

        if not in_group:
            message = "NOT-IN-GROUP: You do not have access to this collection. Please see your system administrator."

            body = {"code": 400,
                    "message": message,
                    "errors": [message, ]}
            return HttpResponse(json.dumps(body, indent=4, ),
                                content_type="application/json")

        # If search keys have been limited...
        if dac.search_keys:
            search_key_list = shlex.split(dac.search_keys)
            for k in request.GET.keys():

                if k not in search_key_list:
                    message = "Search key %s  is not allowed." % (k)
                    body = {"code": 400,
                            "message": k,
                            "errors": [message, ]}

                    return HttpResponse(json.dumps(body, indent=4, ),
                                        content_type="application/json")

        return func(request, *args, **kwargs)

    return update_wrapper(wrapper, func)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def kickout_401(reason, status_code=401):
    response = OrderedDict()
    response["code"] = status_code
    response["status"] = "Authentication error"
    response["errors"] = [reason, ]
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")


def kickout_400(reason, status_code=400):
    response = OrderedDict()
    response["code"] = status_code
    response["status"] = "Client error"
    response["errors"] = [reason, ]
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")


def kickout_404(reason, status_code=404):
    response = OrderedDict()
    response["code"] = status_code
    response["status"] = "NOT FOUND"
    response["errors"] = [reason, ]
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")


def kickout_500(reason, status_code=500):
    response = OrderedDict()
    response["code"] = status_code
    response["status"] = "SERVER SIDE ERROR"
    response["errors"] = [reason, ]
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")
