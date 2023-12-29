#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
import requests

appid = "f5ccde79"
apisecret = "NTA3NjljY2U3MDc5NTRkNWQyOTBmZWZj"
apikey = "d0a87056ee0c663f91729f7934f9a66e"
class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(this, host, path, schema):
        this.host = host
        this.path = path
        this.schema = schema
        pass


class universalOcr(object):
    def __init__(self):
        self.appid = appid
        self.apikey = apikey
        self.apisecret = apisecret
        self.url = 'http://api.xf-yun.com/v1/private/hh_ocr_recognize_doc'


    def parse_url(self,requset_url):
        stidx = requset_url.index("://")
        host = requset_url[stidx + 3:]
        schema = requset_url[:stidx + 3]
        edidx = host.index("/")
        if edidx <= 0:
            raise AssembleHeaderException("invalid request url:" + requset_url)
        path = host[edidx:]
        host = host[:edidx]
        u = Url(host, path, schema)
        return u

    def get_body(self, file_path):
        # 将payload中数据替换成实际能力内容，参考不同能力接口文档请求数据中payload
        file = open(file_path, 'rb')
        print(file_path)
        buf = file.read()
        body = {
            "header": {
                "app_id": self.appid,
                "status": 3
            },
            "parameter": {
                "hh_ocr_recognize_doc": {
                    "recognizeDocumentRes": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "image": {
                    "encoding": "jpg",
                    "image": str(base64.b64encode(buf), 'utf-8'),
                    "status": 3
                }
            }
        }
        # print(body)
        return body


# build websocket auth request url
def assemble_ws_auth_url(requset_url, method="GET", api_key="", api_secret=""):
    universalOcr1=universalOcr()
    # print('-----1111')
    # print(requset_url)
    u = universalOcr1.parse_url(requset_url)
    # print(u)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    # date = "Mon, 22 Aug 2022 03:26:45 GMT"
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    print("signature:",signature_sha)
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    print("authorization:",authorization)
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }

    return requset_url + "?" + urlencode(values)



# def get_result():
#     request_url = assemble_ws_auth_url(universalOcr.url, "POST", universalOcr.apikey, apisecret)
#     headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'appid': 'APPID'}
#     print(request_url)
#     body = universalOcr.get_body(file_path=file_path)
#     response = requests.post(request_url, data=json.dumps(body), headers=headers)
#     print(response)
#     re = response.content.decode('utf8')
#     str_result = json.loads(re)
#     print("\nresponse-content:", re)
#     if str_result.__contains__('header') and str_result['header']['code'] == 0:
#         renew_text = str_result['payload']['recognizeDocumentRes']['text']
#         print("\ntext解析结果：", str(base64.b64decode(renew_text), 'utf-8'))

def get_result(file_path):
    universalOcr1 = universalOcr()
    # print(universalOcr1.url,universalOcr1.apikey, universalOcr1.apisecret)
    # 修改assemble_ws_auth_url调用以接收file_path参数
    request_url = assemble_ws_auth_url(universalOcr1.url, "POST", universalOcr1.apikey, universalOcr1.apisecret)
    # print(file_path)
    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'appid': 'APPID'}

    # 使用传递进来的file_path
    body = universalOcr1.get_body(file_path)

    # 发送请求
    response = requests.post(request_url, data=json.dumps(body), headers=headers)
    re = response.content.decode('utf8')
    str_result = json.loads(re)
    # print(str_result)
    if str_result.__contains__('header') and str_result['header']['code'] == 0:
        renew_text = str_result['payload']['recognizeDocumentRes']['text']
        return str(base64.b64decode(renew_text), 'utf-8')
    else:
        # 如果API响应包含错误，返回错误信息
        return str_result.get('header', {}).get('message', 'Unknown error')


if __name__ == "__main__":
    # 填写在开放平台申请的APPID、APIKey、APISecret
    appid = "f5ccde79"
    apisecret = "NTA3NjljY2U3MDc5NTRkNWQyOTBmZWZj"
    apikey = "d0a87056ee0c663f91729f7934f9a66e"
    file_path = "../upload/test.jpg"

    universalOcr = universalOcr()
    get_result()
