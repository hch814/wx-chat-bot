# -*- coding: utf-8 -*-
"""
日子相关

@author: hch
@date  : 2021/12/8
"""
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from conf.config import APP_CONF


class DaysReminder:
    TEMPLATE = """{}
[爱心]今天是你们在一起的第{}天
"""

    @staticmethod
    def remind():
        return DaysReminder.TEMPLATE.format(DaysReminder.festival(), DaysReminder.days_together())

    @staticmethod
    def days_together():
        begin = APP_CONF.days.begin

        today = datetime.today().date()
        # today = datetime.strptime('2021-10-03', '%Y-%m-%d').date()
        return (today - begin).days + 1

    @staticmethod
    def festival():
        result = []
        resp = requests.get('https://wannianrili.bmcx.com')
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.content, 'lxml')

        rl_today = soup.find('div', id=f'wnrl_k_you_id_{datetime.today().day - 1}')
        # rl_today = soup.find('div', id=f'wnrl_k_you_id_11')
        lunar_date = rl_today.select('div.wnrl_k_you_id_wnrl_nongli')[0].string
        festival_span = rl_today.find('span', 'wnrl_k_you_id_wnrl_jieri_neirong')
        festivals = [f.string for f in festival_span.find_all(recursive=False)] if festival_span else []
        result.append('农历: ' + lunar_date)
        if festivals:
            result.append('节日: ' + ', '.join(festivals))
        return '\n'.join(result)


if __name__ == '__main__':
    # DaysReminder.days_together()
    print(DaysReminder.remind())
