# -*- coding: utf-8 -*-

import hashlib


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
