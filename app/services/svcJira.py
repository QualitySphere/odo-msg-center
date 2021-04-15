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
    _jira_url = os.getenv('JIRA_URL')
    _jira_user = os.getenv('JIRA_USER')
    _jira_pass = os.getenv('JIRA_PASS')
    if not _jira_url or not _jira_user or not _jira_pass:
        logging.error('Need provide JIRA_URL, JIRA_USER, JIRA_PASS')
        raise AssertionError
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
    # assert _rsp.json().get('StatusCode') == 0
    return _rsp.json()


def change_status():
    pass


if __name__ == '__main__':
    print('This is Python scripts')
