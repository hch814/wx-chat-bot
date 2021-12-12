import logging
import time

import schedule

from config import APP_CONF
from wx import WechatBot


def main():
    logging.basicConfig(filename=APP_CONF.logging.file,
                        level=logging.getLevelName(APP_CONF.logging.level),
                        format=APP_CONF.logging.format)
    bot = WechatBot()

    logging.info('start job...')
    # schedule.every().minute.at(':00').do(bot.report, APP_CONF.wx.user)
    schedule.every().day.at("07:15").do(bot.report, APP_CONF.wx.user)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
