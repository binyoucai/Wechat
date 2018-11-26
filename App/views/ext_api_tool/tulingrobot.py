import requests
import json
import re

from App.settings import TULING_API_KEY, TULING_UER_ID


class Robot:
    def __init__(self):
        self.api = 'http://openapi.tuling123.com/openapi/api/v2'
        self.header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0',
                       'Accept': 'application / json, text / javascript, * / *; q = 0.01'
                       }
    def chat(self,message):
        form ={
                    "perception": {
                        "inputText": {
                            "text": str(message)
                                     }
                                   },
                    "userInfo":{
                        "apiKey":TULING_API_KEY,
                        "userId": TULING_UER_ID}
                    }

        json_data = json.dumps(form)

        response = requests.post(url=self.api,data=json_data,headers =self.header)

        data_str = str(response.json())
        data_strs = re.findall(r"'results'.*'values': {'text': '(.*?)'",data_str,re.S)
        for i in range(len(data_strs)):

            yield data_strs[i]

        data_url = re.findall(r"'results'.*'values': {'url': '(.*?)'", data_str, re.S)
        for m in range(len(data_url)):

            yield data_url[m]
#本模块测试
if __name__ == '__main__':
    while True:
            robot = Robot()
            text = input('主人说：')
            if text == 'Q':
                break
            robot.chat(message=text)





