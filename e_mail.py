# -*- coding: utf-8 -*-
"""
邮件机器人

@author: hch
@date  : 2021/10/5
"""
import logging
import smtplib
from configparser import ConfigParser
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailBot:
    def __init__(self):
        self.cp = ConfigParser()

    def send(self, qrcode):
        self.cp.read('conf/email.conf', encoding='utf-8')
        conf = self.cp['info']
        # 设置服务器所需信息
        # 163邮箱服务器地址
        mail_host = conf['host']
        # 163用户名
        mail_user = conf['user']
        # 密码(部分邮箱为授权码)
        mail_pass = conf['password']
        # 邮件发送方邮箱地址
        sender = conf['sender']
        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receivers = [conf['receiver']]

        message = MIMEMultipart()
        # 设置email信息

        # 邮件主题
        message['Subject'] = 'wx py bot'
        # 发送方信息
        message['From'] = sender
        # 接受方信息
        message['To'] = receivers[0]
        # 邮件内容设置
        message.attach(MIMEText('scan qr to login', 'plain', 'utf-8'))

        picture = MIMEImage(qrcode)
        picture['Content-Type'] = 'application/octet-stream'
        picture['Content-Disposition'] = 'attachment;filename="qr.png"'
        message.attach(picture)

        # 登录并发送邮件
        try:
            smtpObj = smtplib.SMTP_SSL(mail_host)
            # 连接到服务器
            # smtpObj.connect(mail_host, 465)
            # 登录到服务器
            smtpObj.login(mail_user, mail_pass)
            # 发送
            smtpObj.sendmail(sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            logging.info('send qr successful')
        except smtplib.SMTPException as e:
            logging.error(f'failed to send qr: {e}')
