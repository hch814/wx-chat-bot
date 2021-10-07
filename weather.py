# -*- coding: utf-8 -*-
"""
天气爬虫

@author: hch
@date  : 2021/10/5
"""
import json
import logging
import re
import time
from configparser import ConfigParser

import requests
from bs4 import BeautifulSoup

# 温度 气象 空气 指数
template = '''温度: {}
气象: {} 
空气指数: {}
穿衣指数: {}
紫外线指数: {}
'''


class WeatherScraper:
    def query_weather_qq(self, province, city):
        try:
            url = f'https://wis.qq.com/weather/common?source=pc&province={province}&city={city}&weather_type=forecast_24h|air|tips|index&_={int(round(time.time() * 1000))}'
            resp = requests.get(url)
            data = json.loads(resp.text)['data']
            forecast = data['forecast_24h']['1']
            air = data['air']
            index = data['index']
            result = template.format(forecast['min_degree'] + '°C ~ ' + forecast['max_degree'] + '°C',
                                     forecast['day_weather'] + '转' + forecast['night_weather'],
                                     str(air['aqi']) + '(' + air['aqi_name'] + ')',
                                     index['clothes']['info'] + '，' + self.query_wearing_index(city),
                                     index['ultraviolet']['detail'])
            return result
        except Exception as e:
            logging.error(f"failed to query weather: {e}")

    def query_wearing_index(self, city):
        url = 'http://www.weather.com.cn/weather1d/' + self._parse_place(city) + '.shtml'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        # print(resp.text)
        soup = BeautifulSoup(resp.content, 'lxml')
        wearing_index = soup.find("li", id="chuanyi")
        return wearing_index.select('a p')[0].string

    def query_weather(self, city):
        result = ''
        try:
            url = 'http://www.weather.com.cn/weather1d/' + self._parse_place(city) + '.shtml'
            resp = requests.get(url)
            resp.encoding = 'utf-8'
            print(resp.text)
            soup = BeautifulSoup(resp.content, 'lxml')
            today = soup.find("div", id="today")

            # 温度
            temperature_list = today.select("p.tem")
            temp_high = int(temperature_list[0].span.string)
            temp_low = int(temperature_list[1].span.string)
            if temp_high < temp_low:
                t = temp_high
                temp_high = str(temp_low)
                temp_low = str(t)

            # 气象
            weather_list = today.select("p.wea")
            if weather_list[0].string == weather_list[1].string:
                weather = weather_list[0].string
            else:
                weather = weather_list[0].string + "转" + weather_list[1].string

            # 空气
            # aqi = today.find('div', class_='zs pol')
            # print(aqi)

            # result = {"h0": temp_high, "l0": temp_low, "w0": weather}
            result = template.format(temp_low + '°C ~ ' + temp_high + '°C', weather, self.query_air(city), None, None)
        except Exception as e:
            logging.error(f"failed to query weather: {e}")
        return result

    def query_air(self, city):
        try:
            url = f'http://d1.weather.com.cn/aqi_all/{self._parse_place(city)}.html?_={int(round(time.time() * 1000))}'
            resp = requests.get(url, headers={'Referer': 'http://www.weather.com.cn/'})
            resp.encoding = 'utf-8'
            # 😐😀😵
            # print(url)
            # print(resp.text)
            data = re.search('"data":\[(.*)\]', resp.text).group(0)
            data = json.loads(data[data.index('['):data.index(']') + 1])[-2]
            return data['t1'] + ' ' + data['t3'] + '(pm2.5)'
        except Exception as e:
            logging.error(f"failed to query air: {e}")

    def _parse_place(self, city):
        cp = ConfigParser()
        cp.read("conf/city.conf", encoding="utf-8")
        try:
            result = cp.get("city", city)
        except Exception as e:
            print("未查找到该城市！仅支持直辖市、地级市和特别行政区！")
            raise e
        return result


if __name__ == '__main__':
    w = WeatherScraper()
    print(w.query_wearing_index('上海'))
    # w.query_air('北京')
    # w.query_weather_qq('上海市', '上海市')
