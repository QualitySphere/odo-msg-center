#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


import requests
# from urllib.parse import urlparse
import os
import logging
from time import time
from hashlib import sha256
import hmac
from base64 import b64encode
from WorkWeixinRobot.work_weixin_robot import WWXRobot
import yaml
from app.services.svcParser import parse_webhook
from jinja2 import Environment as jj2Environment
from jinja2 import FileSystemLoader as jj2FileSystemLoader
from jinja2.exceptions import TemplateNotFound, UndefinedError


def check_user_value_type():
    """
    检查并确定 config/users.yaml 的用户映射类型
    :return:
    """
    try:
        with open(os.path.join('config', 'users.yaml'), 'r', encoding='utf-8') as f:
            _values = yaml.full_load(f.read())
            return list(_values.keys())[0]
    except Exception as e:
        logging.error("Failed to check user value type\n%s" % e)
        return False


def change_user_value(user):
    """
    查找 config/user.yaml 中的数据并替换当前用户的值
    :param user: webhook 中用户的名称
    :return:
    """
    try:
        with open(os.path.join('config', 'users.yaml'), 'r', encoding='utf-8') as f:
            _values = yaml.full_load(f.read())
            _value_type = list(_values.keys())[0]
            return str(_values[_value_type].get(user))
    except Exception as e:
        logging.error("Failed to get user value\n%s" % e)
        return False


def msg_content(tmpl, body):
    """
    解析处理 body 中的信息，渲染消息模板
    :param tmpl:
    :param body:
    :return:
    """
    _body = parse_webhook(body)
    _sender = _body.get('sender')
    _event = _body.get('event')
    _title = _body.get('title')
    _data = _body.get('content')

    # 开始 # 利用 jinja2 渲染模板
    jj2env = jj2Environment(loader=jj2FileSystemLoader('template'))
    try:
        jj2tmpl = jj2env.get_template(tmpl)
    except TemplateNotFound as e:
        logging.error("Failed to get template")
        raise FileNotFoundError(e.message)
    try:
        _content_raw = jj2tmpl.render(_data)
    except UndefinedError as e:
        logging.error("Failed to render template")
        raise KeyError(e.message)
    # 结束

    # 开始 # 检查内容中是否包含 @用户 信息: 格式有可能为 @user 或者 [~user]
    # 若包含，则检查是否能转换为自定义(如企业微信、飞书、钉钉使用)的 ID
    # 若能转换，则替换原 @用户 字符串，并记录下来
    _users = list()
    for _user in _body.get('users'):
        logging.info('Found user %s in message' % _user)
        if '@%s' % _user in _content_raw:
            _im_user = change_user_value(_user)
            if _im_user:
                logging.info('User %s in IM is %s' % (_user, _im_user))
                _content_raw = _content_raw.replace('@%s' % _user, '@%s' % _im_user)
                _users.append(_im_user)
        if '[~%s]' % _user in _content_raw:
            _im_user = change_user_value(_user)
            if _im_user:
                logging.info('User %s in IM is %s' % (_user, _im_user))
                _content_raw = _content_raw.replace('[~%s]' % _user, '@%s' % _im_user)
                _users.append(_im_user)
    # 结束

    # 开始 # 若有需要 @用户 就替换标题中的 @you
    if len(_users) != 0:
        logging.info('Will attention users in message: %s' % _users)
        _title = _title.replace('@you', '@%s' % ' @'.join(_users))
    # 结束

    # 由于飞书得使用 json object，所以需要把 yaml 模板转成 dict
    if tmpl.startswith('fs-'):
        _content = yaml.full_load(_content_raw)
    else:
        _content = _content_raw
    # 结束

    _msg = {
        "sender": _sender,
        "users": _users,
        "event": _event,
        'title': _title,
        'content': _content,
    }
    # logging.warning(_msg)
    return _msg


def wwx(tmpl, body):
    """
    Work Weixin Robot
    :param tmpl:
    :param body:
    :return:
    """
    # 开始 # 企业微信通知需要使用机器人 key，检查环境变量中是否有 WWX_ROBOT_KEY
    _wwx_key = os.getenv('WWX_ROBOT_KEY')
    if not _wwx_key:
        logging.error('WWX_ROBOT_KEY is required')
        raise EnvironmentError
    # 结束

    _content = msg_content(tmpl, body)
    _wwx = WWXRobot(key=_wwx_key)
    return _wwx.send_markdown(content=_content.get('content'))


def fs(tmpl, body):
    """
    FeiShu Robot
    :param tmpl:
    :param body:
    :return:
    """
    # 开始 # 飞书通知需要使用 token 和 secret, 检查环境变量中是否有 FS_TOKEN 和 FS_SECRET
    _fs_token = os.getenv('FS_TOKEN')
    _fs_secret = os.getenv('FS_SECRET')
    if not _fs_token or not _fs_secret:
        logging.error('FS_TOKEN, FS_SECRET is required')
        raise EnvironmentError
    # 结束

    _content = msg_content(tmpl, body)
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
    _body = {
        "timestamp": _timestamp,
        "sign": b64encode(_sign).decode('utf-8'),
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": _content.get('title'),
                    "content": _content.get('content')
                }
            }
        }
    }
    # 开始 # 如果内容中包含用户，就检查是否需要 at，若需要就在请求体中加上 at 部分
    # 似乎需要用有权限的 API 才能获取飞书用户的 userid，暂不处理该处逻辑
    # 结束
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
    # 开始 # 钉钉通知需要使用 token 和 secret，检查环境变量是否有这两个值
    _dt_token = os.getenv('DT_TOKEN')
    _dt_secret = os.getenv('DT_SECRET')
    if not _dt_token or not _dt_secret:
        logging.error('DT_TOKEN, DT_SECRET is required')
        raise EnvironmentError
    # 结束

    _content = msg_content(tmpl, body)
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
    _body = {
        "msgtype": "markdown",
        "markdown": {
            "title": _content.get('title'),
            "text": _content.get('content')
        }
    }

    # 开始 # 如果内容中包含用户，就检查是否需要 at，若需要就在请求体中加上 at 部分
    if len(_content.get('users')) != 0:
        _user_value_type = check_user_value_type()
        logging.info("IM user type is %s" % _user_value_type)
        if _user_value_type == 'mobile':
            _body["at"] = {
                "atMobiles": _content['users']
            }
        elif _user_value_type == 'userid':
            _body["at"] = {
                "atUserIds": _content['users']
            }
    # 结束

    logging.info('%s POST %s?access_token=%s' % (_content['sender'], _url, _params['access_token']))
    logging.info(_body['markdown'])
    _rsp = requests.post(url=_url, params=_params, headers=_headers, json=_body)
    assert _rsp.status_code == 200
    assert _rsp.json().get('errcode') == 0
    return _rsp.json()


if __name__ == '__main__':
    print('This is Python scripts to SEND ROBOT MESSAGE')
