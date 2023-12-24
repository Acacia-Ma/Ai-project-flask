from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime
from App.api import SparkApi  # 引入之前提供的SparkApi模块
from App.models import *
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

        # 返回状态码和模型回答
        return {"code": 0, "msg": "成功", "data": {"response": SparkApi.answer}}


class ChatSessionResource(Resource):
    # 获取所有聊天会话
    def get(self):
        sessions = ChatItemsModel.query.all()
        session_data = [{
            'id': session.id,
            'chat_id': session.chat_id,
            'username': session.username,
            'model_id': session.model_id,
            'title': session.title,
            'updated_at': ChatHistoryModel.query.filter_by(chat_id=session.chat_id).order_by(ChatHistoryModel.updated_at.desc()).first().updated_at if ChatHistoryModel.query.filter_by(chat_id=session.chat_id).first() else None
        } for session in sessions]
        return jsonify(session_data)

    # 创建新聊天会话
    def post(self):
        data = request.json
        new_session = ChatItemsModel(
            chat_id=data['chat_id'],
            username=data['username'],
            model_id=data.get('model_id'),
            title=data.get('title')
        )
        db.session.add(new_session)
        db.session.commit()
        return {'msg': '会话创建成功', 'id': new_session.id}, 201

    # 删除聊天会话
    def delete(self, chat_id):
        session = ChatItemsModel.query.filter_by(chat_id=chat_id).first()
        if session:
            db.session.delete(session)
            db.session.commit()
            return {'msg': '会话删除成功'}, 200
        return {'msg': '会话未找到'}, 404

class ChatHistoryResource(Resource):
    # 保存聊天记录
    def post(self, chat_id):
        data = request.json
        new_history = ChatHistoryModel(
            chat_id=chat_id,
            username=data['username'],
            type=data['type'],
            Content=data['content'],
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(new_history)
        db.session.commit()
        return {'msg': '聊天记录保存成功', 'id': new_history.id}, 201


