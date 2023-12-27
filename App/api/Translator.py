from flask_restful import Resource
from flask import request
import requests
import datetime
import hashlib
import base64
import hmac
import json

class MachineTranslationResource(Resource):
    class Translator:
        def __init__(self):
            self.APPID = "a5bbd07a"
            self.Secret = "MGVlN2UwMmE5ODE4MzVhMjg1MDM4MzMx"
            self.APIKey = "8f80f900f6ee53ef97c98112b0ca5efa"
            self.Host = "ntrans.xfyun.cn"
            self.RequestUri = "/v2/ots"
            self.url = f"https://{self.Host}{self.RequestUri}"
            self.HttpMethod = "POST"
            self.Algorithm = "hmac-sha256"
            self.HttpProto = "HTTP/1.1"

        def hashlib_sha256(self, res):
            m = hashlib.sha256(res.encode('utf-8')).digest()
            return "SHA-256=" + base64.b64encode(m).decode('utf-8')

        def generate_signature(self, digest, date):
            signature_str = f"host: {self.Host}\n"
            signature_str += f"date: {date}\n"
            signature_str += f"{self.HttpMethod} {self.RequestUri} {self.HttpProto}\n"
            signature_str += f"digest: {digest}"
            signature = hmac.new(self.Secret.encode('utf-8'), signature_str.encode('utf-8'), hashlib.sha256).digest()
            return base64.b64encode(signature).decode('utf-8')

        def http_date(self, dt):
            weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
            month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][dt.month - 1]
            return f"{weekday}, {dt.day:02d} {month} {dt.year} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d} GMT"

        def get_headers(self, body, date):
            digest = self.hashlib_sha256(body)
            signature = self.generate_signature(digest, date)
            auth_header = f'api_key="{self.APIKey}", algorithm="{self.Algorithm}", headers="host date request-line digest", signature="{signature}"'
            return {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Method": self.HttpMethod,
                "Host": self.Host,
                "Date": date,
                "Digest": digest,
                "Authorization": auth_header
            }

        def get_body(self, text, from_lang, to_lang):
            post_data = {
                "common": {"app_id": self.APPID},
                "business": {"from": from_lang, "to": to_lang},
                "data": {"text": base64.b64encode(text.encode('utf-8')).decode('utf-8')}
            }
            return json.dumps(post_data)


    def post(self):
        data = request.get_json()
        source_language = data.get("sourceLanguage")
        target_language = data.get("targetLanguage")
        text_to_translate = data.get("text")
        translator = self.Translator()

        body = translator.get_body(text_to_translate, source_language, target_language)
        date = translator.http_date(datetime.datetime.utcnow())
        headers = translator.get_headers(body, date)
        response = requests.post(url=translator.url, headers=headers, data=body)
        status_code = response.status_code
        if status_code != 200:
           return {"error": "Http requsest failed. Status code: " + str(status_code)}
        else:
            respData = response.json()
            result = respData.get('data',{}).get('result','')
            detectedSourceLanguage = result['from']
            trans = result['trans_result']
            translate = trans['dst']
            return {'code': 0, 'data': {'translatedText':translate,'detectedSourceLanguage':detectedSourceLanguage}, 'msg': '翻译成功'}



