# -*- coding: utf-8 -*-
"""
data access

@author: hch
@date  : 2021/12/8
"""
from config import APP_CONF


class MongoDao:
    def __init__(self):
        print(APP_CONF.wx.user)


if __name__ == '__main__':
    MongoDao()