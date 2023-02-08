# -*- coding: utf-8 -*-
"""
data access

@author: hch
@date  : 2021/12/13
"""
import json

import requests


class DailySentenceScraper:
    @staticmethod
    def daily_sentence():
        resp = requests.get(f'http://sentence.iciba.com/index.php?c=dailysentence&m=getTodaySentence')
        # resp = requests.get(f'http://sentence.iciba.com/index.php?c=dailysentence&m=getdetail&title=2021-12-14')
        resp.encoding = 'utf-8'
        resp_json = json.loads(resp.content)
        return resp_json['content'] + ' - ' + resp_json['note']


if __name__ == '__main__':
    print(DailySentenceScraper.daily_sentence())
