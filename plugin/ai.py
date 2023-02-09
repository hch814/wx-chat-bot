
import logging
import requests
from conf.config import APP_CONF
from core.dao import RedisDao


class AiPlugin:
    sign_url = f'https://openai.weixin.qq.com/openapi/sign/{APP_CONF.wxai.token}'
    ai_url = f'https://openai.weixin.qq.com/openapi/aibot/{APP_CONF.wxai.token}'
    sig_cache_key = 'wxbot:ai:signature'

    def get_sig(self):
        sig = RedisDao.r.get(AiPlugin.sig_cache_key)
        if sig is None:
            logging.info('miss signature cache')
            data = {
                "userid": APP_CONF.wxai.userid
            }
            sig_r = requests.post(AiPlugin.sign_url, data=data).json()
            sig = sig_r['signature']
            RedisDao.r.set(AiPlugin.sig_cache_key, sig, int(sig_r['expiresIn'])-10)
        # print('fetch sig cache')
        return sig

    def ai_replay(self, query):
        ai_payload = {
            "signature": self.get_sig(),
            "query": query
        }
        query_r = requests.post(AiPlugin.ai_url, data=ai_payload).json()
        # print(query_r)
        return query_r['answer'] if query_r['answer'] else '不太明白你的问题呢~'


if __name__ == '__main__':
    ai = AiPlugin()
    print(ai.ai_replay("你是谁"))
