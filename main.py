import logging
import time

import schedule
import yaml

from wx import WechatBot

if __name__ == '__main__':
    with open('conf/app.yml') as f:
        conf = yaml.safe_load(f)
        logging.basicConfig(filename=conf['logging']['file'],
                            level=logging.getLevelName(conf['logging']['level']),
                            format=conf['logging']['format'])
    bot = WechatBot()
    logging.info('start job...')


    def morning():
        with open('conf/app.yml') as f:
            conf = yaml.safe_load(f)
        bot.report(conf['wx']['user'])


    # morning()
    # schedule.every(60).seconds.do(morning)
    schedule.every().day.at("07:15").do(morning)
    while True:
        schedule.run_pending()
        time.sleep(1)
