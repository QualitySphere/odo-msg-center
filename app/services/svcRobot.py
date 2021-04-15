#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


import requests
from urllib.parse import urlparse
import os
import logging
from time import time
from hashlib import sha256
import hmac
from base64 import b64encode
from WorkWeixinRobot.work_weixin_robot import WWXRobot
import yaml
from app.services.svcParser import parse_webhook
import jinja2


def msg_content(tmpl, body):
    """
    解析 body
    :param tmpl:
    :param body:
    :return:
    """
    _body = parse_webhook(body)
    _sender = _body.get('sender')
    _event = _body.get('event')
    _title = _body.get('title')
    _data = _body.get('content')
    jj2env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))
    jj2tmpl = jj2env.get_template(tmpl)
    _content_raw = jj2tmpl.render(_data)
    if tmpl.startswith('fs-'):
        _content = yaml.full_load(_content_raw)
    else:
        _content = _content_raw
    _msg = {
        "sender": _sender,
        "event": _event,
        'title': _title,
        'content': _content,
    }
    logging.warning(_msg)
    return _msg


def wwx(tmpl, body):
    """
    Work Weixin Robot
    :param tmpl:
    :param body:
    :return:
    """
    _wwx_key = os.getenv('WWX_ROBOT_KEY')
    if not _wwx_key:
        logging.error('Need provide WWX_ROBOT_KEY')
        raise AssertionError
    _wwx = WWXRobot(key=_wwx_key)
    _content = msg_content(tmpl, body)
    return _wwx.send_markdown(content=_content.get('content'))


def fs(tmpl, body):
    """
    FeiShu Robot
    :param tmpl:
    :param body:
    :return:
    """
    _fs_token = os.getenv('FS_TOKEN')
    _fs_secret = os.getenv('FS_SECRET')
    if not _fs_token or not _fs_secret:
        logging.error('Need provide FS_TOKEN, FS_SECRET')
        raise AssertionError

    _url = 'https://open.feishu.cn/open-apis/bot/v2/hook/%s' % _fs_token
    _headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    _timestamp = int(time())
    _sign_str = '%s\n%s' % (_timestamp, _fs_secret)
    _sign = hmac.new(
        key=_sign_str.encode('utf-8'),
        msg=''.encode('utf-8'),
        digestmod=sha256
    ).digest()
    _content = msg_content(tmpl, body)
    _body = {
        "timestamp": _timestamp,
        "sign": b64encode(_sign).decode('utf-8'),
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": _content.get('title'),
                    "content": [_content.get('content')]
                }
            }
        }
    }
    logging.info('%s POST %s' % (_content['sender'], _url))
    logging.info(_body['content'])
    _rsp = requests.post(url=_url, headers=_headers, json=_body)
    assert _rsp.status_code == 200
    assert _rsp.json().get('StatusCode') == 0
    return _rsp.json()


def dt(tmpl, body):
    """
    DingTalk Robot
    :param tmpl:
    :param body:
    :return:
    """
    _dt_token = os.getenv('DT_TOKEN')
    _dt_secret = os.getenv('DT_SECRET')
    if not _dt_token or not _dt_secret:
        logging.error('Need provide DT_TOKEN, DT_SECRET')
        raise AssertionError

    _url = 'https://oapi.dingtalk.com/robot/send'
    _headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    _timestamp = int(time() * 1000)
    _sign_str = '%s\n%s' % (_timestamp, _dt_secret)
    _sign = hmac.new(
        key=_dt_secret.encode('utf-8'),
        msg=_sign_str.encode('utf-8'),
        digestmod=sha256
    ).digest()
    _params = {
        "access_token": _dt_token,
        "timestamp": _timestamp,
        "sign": b64encode(_sign).decode('utf-8')
    }
    logging.debug(_params)
    _content = msg_content(tmpl, body)
    _body = {
        "msgtype": "markdown",
        "markdown": {
            "title": _content.get('title'),
            "text": _content.get('content')
        }
    }
    logging.info('%s POST %s?access_token=%s' % (_content['sender'], _url, _params['access_token']))
    logging.info(_body['markdown'])
    _rsp = requests.post(url=_url, params=_params, headers=_headers, json=_body)
    assert _rsp.status_code == 200
    assert _rsp.json().get('errcode') == 0
    return _rsp.json()


if __name__ == '__main__':
    print('This is Python scripts')
