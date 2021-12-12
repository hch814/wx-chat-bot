# -*- coding: utf-8 -*-
"""
data access

@author: hch
@date  : 2021/12/8
"""
from pymongo import MongoClient

from config import APP_CONF


class MongoDao:
    def __init__(self):
        self.client = MongoClient(APP_CONF.mongodb.conn)
        self.db = self.client.get_database('wx_chat_bot')

    def log_msg(self, msg):
        self.db.get_collection('msg').insert_one({
            '_id': msg.msgId,
            'content': msg.content,
            'from_user_nick_name': msg.user.nickName,
            'from_user_name': msg.fromUserName,
            'to_user_name': msg.toUserName,
            'create_time': msg.createTime,
        })


if __name__ == '__main__':
    dao = MongoDao()
    print(dao.client.get_database('wx_chat_bot').get_collection('msg').find_one())
