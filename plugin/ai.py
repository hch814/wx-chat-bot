
import random
import requests
from conf.config import APP_CONF


class AiPlugin:
    sign_url = f'https://openai.weixin.qq.com/openapi/sign/{APP_CONF.wxai.token}'
    ai_url = f'https://openai.weixin.qq.com/openapi/aibot/{APP_CONF.wxai.token}'

    def get_sig(self):
        data = {
            "userid": APP_CONF.wxai.userid
        }
        sig_r = requests.post(AiPlugin.sign_url, data=data).json()
        return sig_r['signature']

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
    ai.ai_replay("你是谁")
