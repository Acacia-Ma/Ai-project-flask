from pprint import pprint

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from datetime import datetime
from App.util import SparkApi
from App.models import *
from App.util import ChatConversation,functions_list

# 全局变量，存储星火大模型的密钥信息和地址
APPID = "fd0f6084"
API_SECRET = "MGY1NjdhYzExNmIwMGEzZWIwNWU1NjJi"
API_KEY = "a7fc595758ba180b6de76c7fd4f51105"
DOMAIN = "general"
SPARK_URL = "ws://spark-api.xf-yun.com/v1.1/chat"

# 星火大模型v1.5
app_id = "fd0f6084"
api_secret = "MGY1NjdhYzExNmIwMGEzZWIwNWU1NjJi"
api_key = "a7fc595758ba180b6de76c7fd4f51105"
domain = "general"
spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"

# 星火大模型v3.0
app_id1 = "af076b92"
api_secret1 = "NTkyYWUzMzQ5MmY2YmY0MjQyNWY5NGUy"
api_key1 = "cb55e35a63d1c8c91bc5ce67e11c7cc5"
domain1 = "generalv3"
spark_url1 = "ws://spark-api.xf-yun.com/v3.1/chat"

# 对话功能，用于与前端交互
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

    @jwt_required()
    def post(self):
        # 从请求中获取问题
        data = request.json
        input_text = data.get('text')
        print('input_text:', input_text)
        # [{'id': '1718875908317', 'text': '您好，我是您的AI智能助手，我会尽力帮助您解决问题。', 'type': 'system'},
        #  {'id': '1718875908317', 'text': '给我大理的天气', 'type': 'user', 'role': '1'}]
        # 将数组处理为大模型格式[
        #         {
        #             "role": "user",
        #             "content": '请帮我查询下最近一封QQ邮箱的内容并解读它，user_email为"912811339@qq.com"，user_pass为"blaxffzvxczfbfhh"'
        #         },
        #         {
        #             "role": "user",
        #             "content": "我要使用QQ邮箱给我的朋友发一封邮件，user_to为'1743936315@qq.com'，subject为'Hello'，user_pass为'blaxffzvxczfbfhh'，user_from为'912811339@qq.com'，message_text为'Hello, I am your friend.'"
        #         }
        #     ]
        message = []
        for item in input_text:
            message.append({"role": item["type"], "content": item["text"]})
        print('message:', message)
        model_value = data.get('model')
        # 检查和更新聊天文本
        question = self.checklen(self.getText("user", input_text))
        # 清空上次的回答
        SparkApi.answer = ""
        Chat_GLM3_answer = ""
        if model_value:
            # 调用星火大模型v1.5或v3.0
            if model_value == "v1.5" or model_value == "v3.0":
                if model_value == "v1.5":
                    print("调用星火大模型v1.5")
                    SparkApi.main(app_id, api_key, api_secret, spark_url, domain, question)
                elif model_value == "v3.0":
                    print("调用星火大模型v3.0")
                    SparkApi.main(app_id1, api_key1, api_secret1, spark_url1, domain1, question)
                # 获取并记录助手的回答
                self.getText("assistant", SparkApi.answer)
                # 返回状态码和模型回答
                return {"code": 0, "msg": "成功", "data": {"response": SparkApi.answer}}
            if model_value == "glm-4" or model_value == "glm-4-0520" or model_value == "glm-3-turbo":
                # 调用glm3模型
                conv = ChatConversation(model = model_value)
                conv.messages = message
                Chat_GLM3_answer = conv.run(functions_list=functions_list)
                # 如果大模型回答为空，或者回答为None
                if Chat_GLM3_answer == "" or Chat_GLM3_answer is None:
                    # 返回状态码 和 错误信息
                    return {"code": 0, "msg": "成功", "data": {"response": "对不起，我不明白您的问题。"}}
                # 输出回答
                else:
                    print("Chat_GLM3_answer:", Chat_GLM3_answer)
                    # 返回状态码和模型回答
                    return {"code": 0, "msg": "成功", "data": {"response": Chat_GLM3_answer}}
        else:
            # 返回错误信息
            return {"code": 400, "msg": "模型参数错误,请选择模型版本"}


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
            'updated_at': ChatHistoryModel.query.filter_by(chat_id=session.chat_id).order_by(
                ChatHistoryModel.updated_at.desc()).first().updated_at if ChatHistoryModel.query.filter_by(
                chat_id=session.chat_id).first() else None
        } for session in sessions]
        # print(session_data)
        # return jsonify(session_data)
        return {"code": 0, "msg": "成功获取到所有聊天会话", "data": session_data}

    # 创建新聊天会话
    @jwt_required()
    def post(self):
        data = request.json
        print(''.center(100, '-'))
        print('data:', data)
        print(''.center(100, '-'))
        # 创建并添加 ChatItemsModel 实例
        model_id = 3
        model_txt = data.get('model')
        if model_txt == "v1.5":
            model_id = 1
        elif model_txt == "v3.0":
            model_id = 2
        elif model_txt == "glm-4":
            model_id = 'glm-4'
        elif model_txt == "glm-4-0520":
            model_id = 'glm-4-0520'
        elif model_txt == "glm-3-turbo":
            model_id = 'glm-3-turbo'
        else:
            return {"code": 400, "msg": "模型参数错误,请选择模型版本"}
        # 添加 ChatItemsModel 实例
        new_session = ChatItemsModel(
            chat_id=data['chat_id'],
            username=data['username'],
            model_id=model_id,
            title=data.get('title'),
            # 添加角色ID.从前端获取，如果没有则默认为1
            role_id=data.get('content', 1),
        )
        db.session.add(new_session)
        # 根据role_id 添加初始化消息,从数据库中获取role_id对应的角色提示词
        content = RoleModel.query.filter_by(id=new_session.role_id).first().content
        new_history = ChatHistoryModel(
            chat_id=data['chat_id'],
            username=data['username'],
            type='system',  # 消息类型为系统
            Content= content,
            # 初始化消息内容
            role= data.get('content'),
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(new_history)
        # 提交数据库变更
        db.session.commit()
        # 输出创建的会话信息
        print(''.center(100, '-'))
        print('new_session:', new_session)
        print('new_history:', new_history)
        # 返回成功响应
        return {"code": 0, "msg": "会话创建成功", "data": {"updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}

    # 删除聊天会话和对应的聊天记录
    @jwt_required()
    def delete(self, chat_id):
        session = ChatItemsModel.query.filter_by(chat_id=chat_id).first()
        session_history = ChatHistoryModel.query.filter_by(chat_id=chat_id).all()
        if session:
            for history in session_history:
                db.session.delete(history)
            db.session.delete(session)
            db.session.commit()
            return {"code": 0, "msg": "会话删除成功"}
        return {"code": 404, "msg": "会话未找到"}

    # 修改会话名称
    @jwt_required()
    def put(self, chat_id):
        data = request.json
        print(chat_id, data['title'])
        session = ChatItemsModel.query.filter_by(chat_id=chat_id).first()
        if session:
            session.title = data['title']
            db.session.commit()
            return {"code": 0, "msg": "会话修改成功"}
        return {"code": 404, "msg": "会话未找到"}


class ChatHistoryResource(Resource):
    # 保存聊天记录
    @jwt_required()
    def post(self, chat_id):
        data = request.json
        # 输出请求数据
        print(''.center(100, '-'))
        print('data:', data)
        print(''.center(100, '-'))
        new_history = ChatHistoryModel(
            chat_id=data['id'],
            username=get_jwt_identity(),
            # type 为消息类型，如'user'表示用户消息，'assistant'表示助手消息
            type=data['type'],
            Content=data['text'],
            # role 为角色
            role = data['role'],
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
        # 查询与该用户名相关联的聊天会话使用的模型
        session = ChatItemsModel.query.filter_by(chat_id=chat_id).first()
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
            'updated_at': history.updated_at,
            'model': session.model_id
        } for history in histories]
        # print(session_data)
        # return jsonify(session_data)
        return {"code": 0, "msg": "成功获取到所有聊天记录", "data": history_data}
