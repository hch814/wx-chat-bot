# -*- coding: utf-8 -*-
"""
微信机器人

@author: hch
@date  : 2021/10/5
"""
import logging
import time

import itchat

from config import APP_CONF
from e_mail import EmailBot
from weather import WeatherScraper


class WechatBot:
    MSG_TEMPLATE = '''今天是{}

今天也要是元气满满的一天哦

✨天气情况：
{}
'''
    _store = 'bot.pkl'

    def __init__(self):
        self.bot = itchat.new_instance()
        self.email = EmailBot()
        self.weather = WeatherScraper()
        self.login(True)

    def login(self, email):
        if email:
            self.bot.auto_login(enableCmdQR=2, statusStorageDir=WechatBot._store, loginCallback=self._on_login,
                                qrCallback=self._on_qr, exitCallback=self._on_exit)
        else:
            self.bot.auto_login(enableCmdQR=2, statusStorageDir=WechatBot._store, loginCallback=self._on_login, )
        self.auto_replay()

    def auto_replay(self):
        # print(self.bot.get_friends())
        # print(self.bot.get_chatrooms())

        @self.bot.msg_register(itchat.content.TEXT)
        def replay(msg):
            print(msg)
            return msg.user.nickName + ":" + msg.text

        self.bot.run(blockThread=False)

    def report(self, user):
        try:
            if not self.bot.alive:
                self.login(True)
            # self.bot.search_friends(remarkName=user)[0].send(template.format(self.counter))
            self.bot.search_friends(nickName=user)[0].send(
                WechatBot.MSG_TEMPLATE.format(time.strftime("%Y-%m-%d %A", time.localtime()),
                                              self.weather.query_weather_qq('上海市', '上海市'))
            )
        except IndexError:
            logging.error(f"no such user: {user}")
        except Exception as e:
            logging.error(e)

    def report_group(self, group_name):
        try:
            self.bot.search_chatrooms(name=group_name)[0].send('🤖测试{}[旺柴]'.format(1))
        except IndexError:
            logging.error(f"no such group: {group_name}")
        except Exception as e:
            logging.error(e)

    def _on_login(self):
        logging.info(f'wechat login successfully')
        self.bot.search_friends(nickName=APP_CONF.wx.user)[0].send('【提示】wx-chat-bot已登录')

    def _on_exit(self):
        logging.warning(f'wechat exit...')

    def _on_qr(self, uuid, status, qrcode):
        # logging.info(f'qr: {status} {uuid} {qrcode}')
        if status == '0':
            self.email.send(qrcode)
