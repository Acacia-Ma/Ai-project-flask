import json

from App.exts import db


class Api_key(db.Model):
    __tablename__ = "api_key"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform = db.Column(db.String(40), nullable=False)
    value = db.Column(db.String(255), nullable=False)


class ChatItemsModel(db.Model):
    __tablename__ = "chat_items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    model_id = db.Column(db.Integer)
    title = db.Column(db.String(100))


class ChatModels(db.Model):
    __tablename__ = "chat_models"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform = db.Column(db.String(40), nullable=False)  # 平台
    name = db.Column(db.String(255), nullable=False)  # 模型名称
    value = db.Column(db.String(255), nullable=False)  # 模型值
    enabled = db.Column(db.Boolean, nullable=False)  # 是否启用


class ChatHistoryModel(db.Model):
    __tablename__ = "chat_history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    Content = db.Column(db.UnicodeText)
    token = db.Column(db.Integer, default=0)
    role = db.Column(db.String(50), default='user')
    use_context = db.Column(db.Boolean, default=1)
    created_at = db.Column(db.String(100))
    updated_at = db.Column(db.String(100))
