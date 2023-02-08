
import random
import requests


class AiPlugin:
    api_url = 'http://www.tuling123.com/openapi/api'
    api_key = ['8edce3ce905a4c1dbb965e6b35c3834d',
               'eb720a8970964f3f855d863d24406576',
               '1107d5601866433dba9599fac1bc0083']

    def ai_replay(self, msg):
        key = random.choice(AiPlugin.api_key)
        data = {
            'key': key,  # 如果这个Tuling Key不能用，那就换一个
            'info': msg,  # 这是我们发出去的消息
            'userid': 'wechat-robot',  # 这里你想改什么都可以
        }
        r = requests.post(AiPlugin.api_url, data=data)
        print(r.content)
        # if r['code'] == 40004 and len(AiPlugin.api_key) > 1:
        #     AiPlugin.api_key.remove(key)
        #     return self.ai_replay(msg)
        # return r['text']

if __name__ == '__main__':
    ai = AiPlugin()
    ai.ai_replay("你是谁")