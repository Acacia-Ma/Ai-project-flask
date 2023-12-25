from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
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
    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        print("当前用户:", username)
        # 查询与该用户名相关联的聊天会话
        sessions = ChatItemsModel.query.filter_by(username=username).all()
        session_data = [{
            'id': session.id,
            'chat_id': session.chat_id,
            'username': session.username,
            'model_id': session.model_id,
            'title': session.title,
            'updated_at': ChatHistoryModel.query.filter_by(chat_id=session.chat_id).order_by(ChatHistoryModel.updated_at.desc()).first().updated_at if ChatHistoryModel.query.filter_by(chat_id=session.chat_id).first() else None
        } for session in sessions]
        # print(session_data)
        # return jsonify(session_data)
        return {"code": 0, "msg": "成功获取到所有聊天会话", "data": session_data}

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
        return {"code": 0, "msg": "会话创建成功", "data": {"id": new_session.id}}

    # 删除聊天会话
    def delete(self, chat_id):
        session = ChatItemsModel.query.filter_by(chat_id=chat_id).first()
        if session:
            db.session.delete(session)
            db.session.commit()
            return {"code": 0, "msg": "会话删除成功"}
        return {"code": 404, "msg": "会话未找到"}

    # 修改会话名称
    def put(self, chat_id):
        data = request.json
        print(chat_id,data['title'])
        session = ChatItemsModel.query.filter_by(chat_id=chat_id).first()
        if session:
            session.title = data['title']
            db.session.commit()
            return {"code": 0, "msg": "会话删除成功"}
        return {"code": 404, "msg": "会话未找到"}

class ChatHistoryResource(Resource):
    # 保存聊天记录
    @jwt_required()
    def post(self, chat_id):
        data = request.json
        print(data)
        new_history = ChatHistoryModel(
            chat_id=data['id'],
            username=get_jwt_identity(),
            type=data['type'],
            Content=data['text'],
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(new_history)
        db.session.commit()
        return {"code": 0, "msg": "聊天记录保存成功", "data": {"id": new_history.id}}

    # 获取指定聊天会话的历史记录
    @jwt_required()
    def get(self, chat_id):
        username = get_jwt_identity()
        print("当前用户:", username)
        # 查询与该用户名相关联的聊天会话
        histories = ChatHistoryModel.query.filter_by(chat_id=chat_id).all()
        history_data = [{
            'id': history.id,
            'chat_id': history.chat_id,
            'username': history.username,
            'type': history.type,
            'text': history.Content,
            'token': history.token,
            'role': history.role,
            'use_context': history.use_context,
            'created_at': history.created_at,
            'updated_at': history.updated_at
        } for history in histories]
        # print(session_data)
        # return jsonify(session_data)
        return {"code": 0, "msg": "成功获取到所有聊天记录", "data": history_data}


