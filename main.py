import logging
import time

import schedule
import yaml

from wx import WechatBot


def report(bot):
    with open('conf/app.yml') as f:
        conf = yaml.load(f)
    bot.report(conf['wx']['user'])


if __name__ == '__main__':
    with open('conf/app.yml') as f:
        conf = yaml.load(f)
        logging.basicConfig(filename=conf['logging']['file'],
                            level=logging.getLevelName(conf['logging']['level']),
                            format=conf['logging']['format'])
    bot = WechatBot()
    logging.info('start job...')
    # schedule.every(5).seconds.do(report, bot)
    schedule.every().day.at("07:15").do(report, bot)
    while True:
        schedule.run_pending()
        time.sleep(1)
