#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


from app.services import svcRobot
import logging


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


def wwx(tmpl, body):
    """
    POST /oapi/robot/wwx
    :param tmpl:
    :param body:
    :return:
    """
    logging.info(body)
    try:
        svcRobot.wwx(tmpl, body)
        return {
            'title': 'Succeed'
        }, 200
    except Exception as e:
        raise Exception(e)


def fs(tmpl, body):
    """
    POST /oapi/robot/fs
    :param tmpl:
    :param body:
    :return:
    """
    logging.info(body)
    try:
        svcRobot.fs(tmpl, body)
        return {
            'title': 'Succeed'
        }, 200
    except Exception as e:
        raise Exception(e)


def dt(tmpl, body):
    """
    POST /oapi/robot/dt
    :param tmpl:
    :param body:
    :return:
    """
    logging.info(body)
    try:
        svcRobot.dt(tmpl, body)
        return {
            'title': 'Succeed'
        }, 200
    except Exception as e:
        raise Exception(e)


if __name__ == '__main__':
    print('This is Python scripts')
