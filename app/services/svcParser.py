#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


import os
import yaml
import logging


class OdoParse(object):
    def __init__(self, webhook_body):
        self.webhook_body = webhook_body
        self.webhook_sender = str()
        self.webhook_event = str()
        self.webhook_title = str()
        self.webhook_content = dict()

    def parse_sender(self):
        if 'self' in self.webhook_body.keys() and \
                'key' in self.webhook_body.keys() and \
                'fields' in self.webhook_body.keys():
            self.webhook_sender = 'a4j'
            logging.info('Sender is Automation for Jira')
            return True
        if 'timestamp' in self.webhook_body.keys() and \
                'webhookEvent' in self.webhook_body.keys() and \
                'issue_event_type_name' in self.webhook_body.keys() and \
                'user' in self.webhook_body.keys() and \
                'issue' in self.webhook_body.keys() and \
                'comment' in self.webhook_body.keys():
            self.webhook_sender = 'jira'
            logging.info('Sender is Jira Webhook')
            return True
        if 'type' in self.webhook_body.keys() and \
                'occur_at' in self.webhook_body.keys() and \
                'operator' in self.webhook_body.keys() and \
                'event_data' in self.webhook_body.keys():
            self.webhook_sender = 'harbor'
            logging.info('Sender is Harbor')
            return True

    def parse_jira_webhook(self):
        self.webhook_event = self.webhook_body['webhookEvent'].replace('jira:', '')
        self.webhook_title = '%s %s' % (
            self.webhook_body['issue']['key'],
            self.webhook_body['issue']['fields']['summary']
        )
        self.webhook_content = self.webhook_body
        return True

    def parse_jira_a4j_webhook(self):
        if self.webhook_body['changelog']['total'] == 0:
            self.webhook_event = 'create'
        else:
            self.webhook_event = 'update'
        self.webhook_title = '%s %s' % (self.webhook_body.get('key'), self.webhook_body.get('fields').get('summary'))
        self.webhook_content = self.webhook_body
        return True

    def parse_gitlab_webhook(self):
        pass

    def parse_harbor_webhook(self):
        pass

    def parse_webhook(self):
        if self.webhook_sender == "a4j":
            self.parse_jira_a4j_webhook()
        elif self.webhook_sender == "jira":
            self.parse_jira_webhook()
        elif self.webhook_sender == "harbor":
            self.parse_harbor_webhook()
        elif self.webhook_sender == "gitlab":
            self.parse_gitlab_webhook()
        return {
            "sender": self.webhook_sender,
            "event": self.webhook_event,
            "title": self.webhook_title,
            "content": self.webhook_content,
        }


def parse_webhook(webhook_body):
    odo_parse = OdoParse(webhook_body)
    odo_parse.parse_sender()
    return odo_parse.parse_webhook()


if __name__ == '__main__':
    print('This is Python scripts')
