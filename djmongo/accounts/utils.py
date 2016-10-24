#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import json
from django.contrib.auth import login
from .httpauth import HttpBasicAuthentication
from .models import Permission


def user_permissions(request):
    try:
        p = Permission.objects.filter(user=request.user)
        pl = []
        for i in p:
            pl.append(i.permission_name)
        return tuple(pl)
    except(Permission.DoesNotExist):
        return ()


def authorize(request):
    a = HttpBasicAuthentication()
    if a.is_authenticated(request):
        login(request, request.user)
        auth = True
    else:
        if request.user.is_authenticated():
            auth = True
        else:
            auth = False
    return auth


def unauthorized_json_response(additional_info=None):
    body = {
        "code": 401,
        "message": "Unauthorized - Your account credentials were invalid.",
        "errors": [
            "Unauthorized - Your account credentials were invalid.",
        ]}
    if additional_info:
        body['message'] = "%s %s" % (body['message'], additional_info)
    body = json.dumps(body, indent=4, )
    return body
