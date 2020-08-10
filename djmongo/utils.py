#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import json


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


def json_response_400(error=""):
    body = {"code": 400,
            "message": "Client Error",
            "errors": [error, ]
            }
    body = json.dumps(body, indent=4, )
    return body


def json_response_404(error=""):
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
