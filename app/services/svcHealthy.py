#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


import logging


def black_hole(headers, body):
    """
    Print webhook request
    :param headers:
    :param body:
    :return:
    """
    logging.warning(headers)
    logging.warning(body)
    return True


if __name__ == '__main__':
    print('This is Python scripts')
