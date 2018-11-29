# -*- coding: utf-8 -*-

import hashlib


def get_md5(str):
    """
    计算md5
    :param str: 加密的明文
    :return: 密文
    """
    m = hashlib.md5()
    m.update(str.encode("UTF-8"))
    return m.hexdigest()
