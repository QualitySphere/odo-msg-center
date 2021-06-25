#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


import os
import yaml
import logging


CONFIG_ENV_FILE = os.path.join('config', 'env.yaml')
CONFIG_USERS_FILE = os.path.join('config', 'users.yaml')


class OdoParse(object):
    def __init__(self, webhook_headers, webhook_body):
        self.webhook_headers = webhook_headers
        self.webhook_body = webhook_body
        self.webhook_sender = str()
        self.webhook_users = list()
        self.webhook_event = str()
        self.webhook_title = str()
        self.webhook_content = dict()

    def parse_sender(self):
        if self.webhook_headers.get('X-Gitlab-Event'):
            self.webhook_sender = 'gitlab'
            logging.info('Sender is GitLab')
            return True
        if self.webhook_headers.get('User-Agent'):
            if 'Automation for Jira' in self.webhook_headers['User-Agent']:
                self.webhook_sender = 'a4j'
                logging.info('Sender is Automation for Jira')
            elif 'Atlassian HttpClient' in self.webhook_headers['User-Agent']:
                self.webhook_sender = 'jira'
                logging.info('Sender is Jira Webhook')
            elif 'Go-http-client' in self.webhook_headers['User-Agent']:
                self.webhook_sender = 'harbor'
                logging.info('Sender is Harbor')
            return True

    def parse_user(self, key_smart_path: str):
        """
        解析 webhook 中的用户信息
        :param key_smart_path: user key path. e.g. 'comment.author.name'
        :return:
        """
        try:
            _user = self.webhook_body
            for _key in key_smart_path.split('.'):
                _user = _user[_key]
            if _user:
                logging.info('Found user %s in origin webhook' % _user)
                self.webhook_users.append(_user)
        except Exception as e:
            logging.info('User path not found\n%s' % e)

    def parse_jira_webhook(self):
        self.webhook_event = self.webhook_body['webhookEvent'].replace('jira:', '').replace('_', '').capitalize()
        self.webhook_title = 'Jira @you'
        self.webhook_content = self.webhook_body
        self.parse_user('comment.author.name')
        self.parse_user('comment.updateAuthor.name')
        # 为 评论的 jira webhook 单独处理
        try:
            for _item in self.webhook_body['comment']['body'].split():
                if _item.startswith('[~') and _item.endswith(']'):
                    self.webhook_users.append(_item.replace('[~', '').replace(']', ''))
        except Exception as e:
            logging.info('User info not found\n%s' % e)
        return True

    def parse_jira_a4j_webhook(self):
        if self.webhook_body['changelog']['total'] == 0:
            self.webhook_event = 'Create'
        else:
            self.webhook_event = 'Update'
        self.webhook_title = 'Jira @you'
        self.webhook_content = self.webhook_body
        self.parse_user('fields.creator.name')
        self.parse_user('fields.reporter.name')
        self.parse_user('fields.assignee.name')
        return True

    def parse_gitlab_webhook(self):
        self.webhook_title = 'GitLab @you'
        self.webhook_content = self.webhook_body
        return True

    def parse_harbor_webhook(self):
        self.webhook_event = self.webhook_body['type'].replace('_', ' ').capitalize()
        self.webhook_title = 'Harbor @you'
        self.webhook_content = self.webhook_body
        return True

    def parse_custom_webhook(self):
        if self.webhook_body.get('event'):
            self.webhook_event = self.webhook_body.get('event')
        if not self.webhook_body.get('sender'):
            self.webhook_body['sender'] = 'MSG Center'
        self.webhook_title = '%s @you' % self.webhook_body['sender']
        self.webhook_content = self.webhook_body
        return True

    def parse_webhook(self):
        if self.webhook_sender == "a4j":
            self.parse_jira_a4j_webhook()
        elif self.webhook_sender == "jira":
            self.parse_jira_webhook()
        elif self.webhook_sender == "harbor":
            self.parse_harbor_webhook()
        elif self.webhook_sender == "gitlab":
            self.parse_gitlab_webhook()
        else:
            self.parse_custom_webhook()
        return {
            "sender": self.webhook_sender,
            "users": list(set(self.webhook_users)),
            "event": self.webhook_event,
            "title": self.webhook_title,
            "content": self.webhook_content,
        }


def parse_webhook(webhook_headers, webhook_body):
    odo_parse = OdoParse(webhook_headers, webhook_body)
    odo_parse.parse_sender()
    return odo_parse.parse_webhook()


def get_env_config(env_name):
    """
    获取环境变量配置文件 config/env.yaml 中的环境变量
    :param env_name:
    :return:
    """
    with open(CONFIG_ENV_FILE, 'r', encoding='utf-8') as f:
        return yaml.full_load(f.read()).get(env_name)


def get_im_user(user):
    """
    查找 config/users.yaml 中当前用户的值
    :param user: webhook 中用户的名称
    :return:
    """
    with open(CONFIG_USERS_FILE, 'r', encoding='utf-8') as f:
        return yaml.full_load(f.read()).get(user)


if __name__ == '__main__':
    print('This is Python scripts to PARSE WEBHOOK')
