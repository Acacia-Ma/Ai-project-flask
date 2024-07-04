from pprint import pprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from datetime import datetime
from App.util import SparkApi
from App.models import *
from App.util import ChatConversation,functions_list
appid = "b9cc1250"     #填写控制台中获取的 APPID 信息
api_secret = "NGYwYTI2ZTI2NDUzNGYyOTM3YTAwY2I3"   #填写控制台中获取的 APISecret 信息
api_key ="ee8b60bd0bac6b49512773051053981c"    #填写控制台中获取的 APIKey 信息

domain = "generalv3.5"      # Max版本
domain_pro = "generalv3"       # Pro版本
domain_Lite = "general"         # Lite版本
domain_Ultra = "4.0Ultra"        # 4.0超级版

Spark_url_Max = "wss://spark-api.xf-yun.com/v3.5/chat"   # Max服务地址
Spark_url_Pro = "wss://spark-api.xf-yun.com/v3.1/chat"  # Pro服务地址
Spark_url_Lite = "wss://spark-api.xf-yun.com/v1.1/chat"  # Lite服务地址
Spark_url_Ultra = "wss://spark-api.xf-yun.com/v4.0/chat"  # 4.0超级版服务地址
# 对话功能，用于与前端交互
class Chat(Resource):
    def __init__(self):
        self.text = []

    def getText(self, role, content):
        jsoncon = {}
        jsoncon["role"] = role
        jsoncon["content"] = content
        self.text.append(jsoncon)
        return self.text

    def getlength(self, text):
        length = 0
        for content in text:
            temp = content["content"]
            leng = len(temp)
            length += leng
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
        model_mapping = {
            'Lite': (Spark_url_Lite, domain_Lite),
            'Pro': (Spark_url_Pro, domain_pro),
            'Max': (Spark_url_Max, domain),
            'Ultra': (Spark_url_Ultra, domain_Ultra),
            'glm-4': 'glm-4',
            'glm-4-0520': 'glm-4-0520',
            'glm-3-turbo': 'glm-3-turbo'
        }

        model_value = data.get('model')
        message = [{"role": item["type"], "content": item["text"]} for item in input_text]

        if model_value in model_mapping:
            if isinstance(model_mapping[model_value], tuple):
                print(f"调用星火大模型{model_value}")
                SparkApi.main(appid, api_key, api_secret, *model_mapping[model_value], message)
                self.getText("assistant", SparkApi.answer)
                return {"code": 0, "msg": "成功", "data": {"response": SparkApi.answer}}
            else:
                conv = ChatConversation(model=model_value)
                conv.messages = message
                Chat_GLM3_answer = conv.run(functions_list=functions_list)
                if not Chat_GLM3_answer:
                    return {"code": 0, "msg": "成功", "data": {"response": "对不起，我不明白您的问题。"}}
                else:
                    return {"code": 0, "msg": "成功", "data": {"response": Chat_GLM3_answer}}
        else:
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
        model_mapping = {
            'Lite': 'Lite',
            'Pro': 'Pro',
            'Max': 'Max',
            'Ultra': 'Ultra',
            'glm-4': 'glm-4',
            'glm-4-0520': 'glm-4-0520',
            'glm-3-turbo': 'glm-3-turbo'
        }
        model_id = model_mapping.get(data.get('model'))
        if model_id is None:
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
        print(len(session_history))
        if session:
            for history in session_history:
                db.session.delete(history)
                db.session.commit()
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
        print(''.center(100, '-'))
        print('new_history:', new_history)
        print(''.center(100, '-'))
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
        return {"code": 0, "msg": "成功获取到所有聊天记录", "data": history_data}
