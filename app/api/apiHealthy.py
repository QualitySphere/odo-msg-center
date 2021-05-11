#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import request
from app.services import svcHealthy


def swagger_ui():
    """
    GET /opai/ui
    :return:
    """
    return True


def healthy():
    """
    GET /oapi/healthy
    :return:
    """
    try:
        return {
            'status': 'Healthy'
        }, 200
    except Exception as e:
        raise Exception(e)


def black_hole(body):
    """
    POST /oapi/blackhole
    :return:
    """
    try:
        svcHealthy.black_hole(request.headers, body)
        return {}, 204
    except Exception as e:
        raise Exception(e)


if __name__ == '__main__':
    print('This is Healthy API scripts')
