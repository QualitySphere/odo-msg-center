#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


import requests
import os
import logging
from jinja2 import Environment as jj2Environment
from jinja2 import FileSystemLoader as jj2FileSystemLoader
from jinja2.exceptions import TemplateNotFound, UndefinedError


def jira_comment(tmpl, body):
    """
    解析处理 body 长的信息，渲染 jira 评论模板
    :param tmpl:
    :param body:
    :return:
    """
    jj2env = jj2Environment(loader=jj2FileSystemLoader('template'))
    try:
        jj2tmpl = jj2env.get_template(tmpl)
    except TemplateNotFound as e:
        logging.error(e.message)
        raise FileNotFoundError("Failed to get template")
    try:
        _content = jj2tmpl.render(body)
    except UndefinedError as e:
        logging.error(e.message)
        raise KeyError("Failed to render template")
    return _content


def add_comment(tmpl, key, body):
    """
    Add Jira Issue Comment
    :param tmpl:
    :param key: Jira issue key
    :param body:
    :return:
    """
    # 开始 # 要添加 jira 评论，需要使用 Jira 账密操作 Jira，检查环境变量中是否有 JIRA_URL, JIRA_USER, JIRA_PASS
    _jira_url = os.getenv('JIRA_URL')
    _jira_user = os.getenv('JIRA_USER')
    _jira_pass = os.getenv('JIRA_PASS')
    if not _jira_url or not _jira_user or not _jira_pass:
        logging.error('JIRA_URL, JIRA_USER, JIRA_PASS is required')
        raise EnvironmentError
    # 结束

    _url = '%s/rest/api/2/issue/%s/comment' % (_jira_url, key)
    _headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    _body = {
        "body": jira_comment(tmpl, body)
    }
    logging.info('POST %s' % _url)
    logging.info(_body['body'])
    _rsp = requests.post(url=_url, headers=_headers, json=_body)
    assert _rsp.status_code == 200
    return _rsp.json()


def change_status():
    pass


if __name__ == '__main__':
    print('This is Python scripts to OPERATE JIRA ISSUE')
