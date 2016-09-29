#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import json
import string
import random
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from datetime import date


def random_string(length=6, alphabet=string.letters + string.digits):
    """
    Return a random string of given length and alphabet.

    Default alphabet is url-friendly (base62).
    This method lifted from @shazow - thanx man.
    """
    return ''.join([random.choice(alphabet) for i in xrange(length)])


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


def json_response_400(errors=""):
    body = {"code": 400,
            "message": "Client Error",
            "errors": [error, ]
            }
    body = json.dumps(body, indent=4, )
    return body


def json_response_404(errors=""):
    body = {"code": 404,
            "message": "Not Found",
            "errors": [error, ]
            }
    body = json.dumps(body, indent=4, )
    return body


def json_response_500(error=""):
    body = {"code": 500,
            "message": "Server Side Error",
            "errors": [error, ]
            }
    body = json.dumps(body, indent=4, )
    return body


def normalize_phone_number(pn):
    try:
        pn = str(pn)
    except:
        return None
    if len(pn) != 10 and len(pn) != 11:
        return None
    try:
        x = int(pn)
    except:
        return None

    if len(pn) == 10:
        pn = "+1%s" % (pn)
    if len(pn) == 11:
        pn = "+%s" % (pn)
    return pn
