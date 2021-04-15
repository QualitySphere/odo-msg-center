#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


from app.services import svcRobot
import logging


def wwx(tmpl, body):
    """
    POST /robot/wwx
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
    POST /robot/fs
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
    POST /robot/dt
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
