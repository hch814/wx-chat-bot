# -*- coding: utf-8 -*-
"""
微信机器人

@author: hch
@date  : 2021/10/5
"""
import logging
import time

import itchat

from e_mail import EmailBot
from weather import WeatherScraper

template = '''今天是{}

今天也要是元气满满的一天哦

✨天气情况：
{}
'''


class WechatBot:
    _store = 'bot.pkl'

    def __init__(self):
        self.bot = itchat.new_instance()
        self.email = EmailBot()
        self.weather = WeatherScraper()
        self.login(True)
        self.counter = 1
        self.register()

    def login(self, email):
        if email:
            self.bot.auto_login(enableCmdQR=2, statusStorageDir=WechatBot._store, loginCallback=self._on_login,
                                qrCallback=self._on_qr)
        else:
            self.bot.auto_login(enableCmdQR=2, statusStorageDir=WechatBot._store, loginCallback=self._on_login, )

    def register(self):
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
                template.format(time.strftime("%Y-%m-%d %A", time.localtime()),
                                self.weather.query_weather_qq('上海市', '上海市'))
            )
            self.counter += 1
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
        logging.info(f'wechat login successful: {self.bot.loginInfo}')

    def _on_qr(self, uuid, status, qrcode):
        # logging.info(f'qr: {status} {uuid} {qrcode}')
        if status == '0':
            self.email.send(qrcode)
