# -*- coding: utf-8 -*-

import hashlib
import re
import datetime


def get_md5(value):
    """
    计算md5
    :param value: 加密的明文
    :return: 密文
    """
    if isinstance(value, str):
        value = value.encode("UTF-8")
    m = hashlib.md5()
    m.update(value)
    return m.hexdigest()


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def format_date(value):
    try:
        create_date = datetime.datetime.strptime(value.replace("·", "").strip(), '%Y/%m/%d').date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def remove_comment_tags(value):
    if '评论' in value:
        return ''
    else:
        return value
