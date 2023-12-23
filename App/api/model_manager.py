from flask import request, jsonify
from flask_restful import Resource
from App.api import SparkApi  # 引入之前提供的SparkApi模块

# 全局变量，存储星火大模型的密钥信息和地址
APPID = "fd0f6084"
API_SECRET = "MGY1NjdhYzExNmIwMGEzZWIwNWU1NjJi"
API_KEY = "a7fc595758ba180b6de76c7fd4f51105"
DOMAIN = "general"
SPARK_URL = "ws://spark-api.xf-yun.com/v1.1/chat"

class Chat(Resource):
    def __init__(self):
        self.text = []

    def getText(self, role, content):
        jsoncon = {"role": role, "content": content}
        self.text.append(jsoncon)
        return self.text

    def getlength(self, text):
        length = 0
        for content in text:
            temp = content["content"]
            length += len(temp)
        return length

    def checklen(self, text):
        while self.getlength(text) > 8000:
            del text[0]
        return text

    def post(self):
        # 从请求中获取问题
        data = request.json
        input_text = data.get('text')

        # 检查和更新聊天文本
        question = self.checklen(self.getText("user", input_text))

        # 清空上次的回答
        SparkApi.answer = ""

        # 调用星火大模型
        SparkApi.main(APPID, API_KEY, API_SECRET, SPARK_URL, DOMAIN, question)

        # 获取并记录助手的回答
        self.getText("assistant", SparkApi.answer)

        # 返回聊天模型的回答
        return jsonify({"response": SparkApi.answer})
