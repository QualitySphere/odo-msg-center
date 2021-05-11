#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


from flask import request
from app.services import svcJira
# import logging


def add_comment(tmpl, key, body):
    """
    POST /oapi/pm/jira/comment
    :param tmpl:
    :param key: JIRA ISSUE KEY
    :param body:
    :return:
    """
    # logging.info(body)
    try:
        svcJira.add_comment(tmpl, key, body)
        return {
            'title': 'Succeed'
        }, 200
    except Exception as e:
        raise Exception(e)


if __name__ == '__main__':
    print('This is Python scripts')
