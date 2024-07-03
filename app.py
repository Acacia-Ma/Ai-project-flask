from App import create_app
from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_socketio import SocketIO, emit
import asyncio
# from App.util import SparkApi
import _thread as thread
import asyncio
from urllib.parse import urlencode
from time import mktime

import websocket
import websockets
import json
import base64
from datetime import datetime
import hashlib
import hmac
from urllib.parse import urlparse
from wsgiref.handlers import format_date_time

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

# ... 其他代码 ...
appid = "b9cc1250"
api_secret = "NGYwYTI2ZTI2NDUzNGYyOTM3YTAwY2I3"
api_key = "ee8b60bd0bac6b49512773051053981c"
answer = ""
domain_35 = "generalv3.5"      # Max版本
domain_pro = "generalv3"       # Pro版本
domain_Lite = "general"         # Lite版本
domain_Ultra = "4.0Ultra"        # 4.0超级版

Spark_url_Max = "wss://spark-api.xf-yun.com/v3.5/chat"   # Max服务地址
Spark_url_Pro = "wss://spark-api.xf-yun.com/v3.1/chat"  # Pro服务地址
Spark_url_Lite = "wss://spark-api.xf-yun.com/v1.1/chat"  # Lite服务地址
Spark_url_Ultra = "wss://spark-api.xf-yun.com/v4.0/chat"  # 4.0超级版服务地址
app = create_app()
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

Spark_url=''
domain=''
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    global Spark_url
    sid = request.sid  # Get the session ID of the client
    # print("Received message:", data)
    # 前端传递的模型参数 : 'Lite', 'Pro', 'Max', 'Ultra
    model = data["model"]
    # 根据模型参数选择对应的Spark_url和domain
    model_mapping = {
        'Lite': (Spark_url_Lite, domain_Lite),
        'Pro': (Spark_url_Pro, domain_pro),
        'Max': (Spark_url_Max, domain_35),
        'Ultra': (Spark_url_Ultra, domain_Ultra)
    }
    # 根据模型参数获取对应的Spark_url和domain
    Spark_url, domain = model_mapping.get(model, (None, None))
    print(f"正在使用{model}模型")
    if Spark_url is None or domain is None:
       # 如果模型参数不在model_mapping中，使用默认的Lite模型
        Spark_url, domain = Spark_url_Lite, domain_Lite
        print(f"大模型参数错误，使用默认的Lite模型")
    # 前端传递的问题
    message_text = data.get("text", "")
    # 前端传递的问题
    message = []
    for item in message_text:
        message.append({"role": item["type"], "content": item["text"]})
    # print("Received message:", message)
    # Run the spark API in a new thread without passing 'sid'
    thread.start_new_thread(run_spark_api_thread, (appid, api_key, api_secret, Spark_url, domain, message, sid))
def run_spark_api_thread(appid, api_key, api_secret, Spark_url, domain, message, sid):
    # Pass 'sid' to the run_spark_api function
    asyncio.run(run_spark_api(appid, api_key, api_secret, Spark_url, domain, message, sid))


async def run_spark_api(appid, api_key, api_secret, Spark_url, domain, message, sid):
    wsParam = Ws_Param(appid, api_key, api_secret, Spark_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    async with websockets.connect(wsUrl) as ws:
        data = json.dumps(gen_params(appid=appid, domain=domain, question=message))
        await ws.send(data)
        try:
            while True:
                response = await ws.recv()
                data = json.loads(response)
                code = data['header']['code']
                if code != 0:
                    print(f'请求错误: {code}, {data}')
                    socketio.emit('error', {'message': f'请求错误: {code}, {data}'})
                    break
                else:
                    sid = data["header"]["sid"]
                    choices = data["payload"]["choices"]
                    status = choices["status"]
                    content = choices["text"][0]["content"]
                    # 发送每个部分的回答给前端，实现流式输出
                    socketio.emit('stream_message', {'answer': content, 'status': status})

                    # 如果对话结束或者有其他结束条件，可以在这里处理
                    if status == 2:
                        break
        except websockets.exceptions.ConnectionClosedOK:
            # 正常关闭连接，不打印任何信息
            pass
        except Exception as e:
            # 其他异常情况，打印错误信息
            print(f'An error occurred: {e}')
            socketio.emit('error', {'message': f'An error occurred: {e}'})
@socketio.on('connect')
def test_connect():
    print("Connected")
    socketio.emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)