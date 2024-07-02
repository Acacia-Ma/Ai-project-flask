import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
import time
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import asyncio
import json
import time
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import socketio
import websocket
import websocket  # 使用websocket_client

answer = ""
sid = ''


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Spark_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(Spark_url).netloc
        self.path = urlparse(Spark_url).path
        self.Spark_url = Spark_url

    # 生成url
    def create_url(self):
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = f"host: {self.host}\ndate: {date}\nGET {self.path} HTTP/1.1"
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 hashlib.sha256).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode('utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')

        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        url = self.Spark_url + '?' + urlencode(v)
        return url


# 异步处理WebSocket错误
async def on_error(ws, error):
    print("### error:", error)
    # 这里可以添加关闭WebSocket连接的代码，或者发送错误消息到前端


# 异步处理WebSocket关闭
async def on_close(ws, *args):
    print("### closed ###")


# 异步处理WebSocket连接建立
async def on_open(ws):
    # 在新线程中运行发送数据的函数
    asyncio.create_task(run(ws))


# 异步运行WebSocket发送数据
async def run(ws):
    data = json.dumps(gen_params(appid=ws.appid, domain=ws.domain, question=ws.question))
    await ws.send(data)


# 异步处理WebSocket消息
async def on_message(ws, message):
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        await ws.close()
    else:
        global sid
        sid = data["header"]["sid"]
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        print(content, end="")
        global answer
        answer += content
        if status == 2:
            await ws.close()


def gen_params(appid, domain, question):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {

            "chat": {
                "domain": domain,
                "temperature": 0.8,
                "max_tokens": 2048,
                "top_k": 5,

                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data


# 修改后的 main 函数，使用 asyncio
async def main(appid, api_key, api_secret, Spark_url, domain, question):
    wsParam = Ws_Param(appid, api_key, api_secret, Spark_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    # 使用异步版本的 WebSocketApp
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open,
                                sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.appid = appid
    ws.question = question
    ws.domain = domain
    # 使用异步的事件循环运行
    await ws.run_forever()


