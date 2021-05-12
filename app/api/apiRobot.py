#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


from flask import request
from app.services import svcRobot
from urllib.parse import unquote
import logging


def __assert_body_filter(body: dict, body_filter):
    if body_filter:
        _fk, _fv = unquote(body_filter).split('=')
        _v = body.copy()
        try:
            for _k in _fk.split('.'):
                # logging.warning(_v)
                if type(_v) is list:
                    _v = _v[int(_k)]
                else:
                    _v = _v[_k]
        except KeyError or TypeError:
            logging.warning(u'过滤条件异常，查找 %s 时出错' % _fk)
            return False
        if _fv not in _v:
            return False
    return True


def list_robot():
    """
    GET /oapi/robot
    :return:
    """
    try:
        return svcRobot.list_robot(), 200
    except Exception as e:
        raise Exception(e)


def list_tmpl():
    """
    GET /oapi/robot/template
    :return:
    """
    try:
        return svcRobot.list_tmpl(), 200
    except Exception as e:
        raise Exception(e)


def get_tmpl(tmpl):
    try:
        return svcRobot.get_tmpl(tmpl), 200
    except Exception as e:
        raise Exception(e)


def wwx(tmpl, body, body_filter=None):
    """
    POST /oapi/robot/wwx
    :param tmpl:
    :param body:
    :param body_filter:
    :return:
    """
    logging.info(body)
    try:
        if __assert_body_filter(body, body_filter):
            svcRobot.wwx(request.headers, tmpl, body)
        else:
            logging.info('Ignore this webhook because of filter %s' % body_filter)
        return {
                   'title': 'Succeed'
               }, 200
    except Exception as e:
        raise Exception(e)


def fs(tmpl, body, body_filter=None):
    """
    POST /oapi/robot/fs
    :param tmpl:
    :param body:
    :param body_filter:
    :return:
    """
    logging.info(body)
    try:
        if __assert_body_filter(body, body_filter):
            svcRobot.fs(request.headers, tmpl, body)
        else:
            logging.info('Ignore this webhook because of %s' % body_filter)
        return {
                   'title': 'Succeed'
               }, 200
    except Exception as e:
        raise Exception(e)


def dt(tmpl, body, body_filter=None):
    """
    POST /oapi/robot/dt
    :param tmpl:
    :param body:
    :param body_filter:
    :return:
    """
    logging.info(body)
    try:
        if __assert_body_filter(body, body_filter):
            svcRobot.dt(request.headers, tmpl, body)
        else:
            logging.info('Ignore this webhook because of %s' % body_filter)
        return {
                   'title': 'Succeed'
               }, 200
    except Exception as e:
        raise Exception(e)


if __name__ == '__main__':
    print('This is Python scripts')
