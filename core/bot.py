# -*- coding: utf-8 -*-
"""
微信机器人

@author: hch
@date  : 2021/10/5
"""
import logging
import random
import time

import itchat
import requests

from conf.config import APP_CONF
from core.dao import MongoDao
from plugin.ai import AiPlugin
from plugin.day import DaysReminder
from core.email import EmailBot
from plugin.sentence import DailySentenceScraper
from plugin.weather import WeatherScraper
from itchat.content import *

class WechatBot:
    MSG_TEMPLATE = '''今天是{}

今天也要是元气满满的一天哦

🌈天气情况：
{}

💬每日一句：
{}

📅日子：
{}
'''
    _store = 'bot.pkl'
    api_url = 'http://www.tuling123.com/openapi/api'
    api_key = ['8edce3ce905a4c1dbb965e6b35c3834d',
               'eb720a8970964f3f855d863d24406576',
               '1107d5601866433dba9599fac1bc0083']

    def __init__(self):
        self.bot = itchat.load_sync_itchat()
        self.weather = WeatherScraper()
        self.dao = MongoDao()
        self.ai = AiPlugin()
        self.login(False)

    def login(self, email):
        if email:
            self.bot.auto_login(hotReload=True, enableCmdQR=2, statusStorageDir=WechatBot._store, loginCallback=self._on_login,
                                qrCallback=self._on_qr, exitCallback=self._on_exit)
        else:
            self.bot.auto_login(hotReload=True, enableCmdQR=2, statusStorageDir=WechatBot._store, loginCallback=self._on_login)
        self.auto_replay()
        self.heartbeat()

    def auto_replay(self):
        # logging.info(self.bot.get_friends())
        # print(self.bot.get_chatrooms())

        @self.bot.msg_register(TEXT)
        def replay_echo(msg):
            logging.info(f'receive msg: {msg}')
            if msg.text == '早安':
                return self.report(msg.user.nickName)
            if msg.text.startswith('echo '):
                msg.user.send(msg.text[5:])
                return msg.text[5:]
            return self.send('HCH', self.ai.ai_replay(msg.text))
            # logging.info(msg)
            # self.dao.log_msg(msg)
            # return msg.user.nickName + ":" + msg.text

        @self.bot.msg_register(TEXT, isGroupChat=True)
        def group_replay(msg):
            if msg.isAt:
                if msg.text.startswith('echo '):
                    msg.user.send(u'@%s\u2005I received: %s' % (msg.actualNickName, msg.text[5:]))
                elif msg.text == '早安':
                    msg.user.send(
                        WechatBot.MSG_TEMPLATE.format(time.strftime("%Y-%m-%d %A", time.localtime()),
                                                      self.weather.query_weather_qq('上海市', '上海市'),
                                                      DailySentenceScraper.daily_sentence(),
                                                      DaysReminder.remind(), )
                    )
                else:
                    msg.user.send(self.ai.ai_replay(msg.text))

        self.bot.run(blockThread=False)

    def send(self, user, msg):
        try:
            user_list = self.bot.search_friends(nickName=user)
            if not user_list:
                user_list = self.bot.search_friends(userName=user)
            user_list[0].send(msg)
        except IndexError:
            logging.error(f"no such user: {user}")
        except Exception as e:
            logging.error(e)

    def heartbeat(self):
        self.bot.send('【heartbeat】wx-chat-bot alive', toUserName='filehelper')

    def report(self, user):
        try:
            if not self.bot.alive:
                # self.login(True)
                logging.warning('wx-chat-bot not alive!')
                return
            self.bot.search_friends(nickName=user)[0].send(
                WechatBot.MSG_TEMPLATE.format(time.strftime("%Y-%m-%d %A", time.localtime()),
                                              self.weather.query_weather_qq('上海市', '上海市'),
                                              DailySentenceScraper.daily_sentence(),
                                              DaysReminder.remind(), )
            )
        except IndexError:
            logging.error(f"no such user: {user}")
        except Exception as e:
            logging.error(e)

    def morning_greeting(self, group_name):
        try:
            if not self.bot.alive:
                # self.login(True)
                logging.warning('wx-chat-bot not alive!')
                return
            self.bot.search_chatrooms(name=group_name)[0].send(
                WechatBot.MSG_TEMPLATE.format(time.strftime("%Y-%m-%d %A", time.localtime()),
                                              self.weather.query_weather_qq('上海市', '上海市'),
                                              DailySentenceScraper.daily_sentence(),
                                              DaysReminder.remind(), )
            )
        except IndexError:
            logging.error(f"no such group: {group_name}")
        except Exception as e:
            logging.error(e)

    def _on_login(self):
        logging.info('wx-chat-bot login successfully')
        self.bot.search_friends(nickName=APP_CONF.wx.user)[0].send('【提示】wx-chat-bot已登录')

    def _on_exit(self):
        logging.warning('wx-chat-bot exit...')
        EmailBot.send_msg('wx-chat-bot exit...')

    def _on_qr(self, uuid, status, qrcode):
        # logging.info(f'qr: {status} {uuid} {qrcode}')
        if status == '0':
            EmailBot.send_qr(qrcode)
