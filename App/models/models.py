import json

from App.exts import db


class Api_key(db.Model):
    __tablename__ = "api_key"
    # 主键，自增长的ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 平台名称，如 "Google", "Facebook" 等
    platform = db.Column(db.String(40), nullable=False)
    # API密钥的值
    value = db.Column(db.String(255), nullable=False)


class ChatItemsModel(db.Model):
    __tablename__ = "chat_items"
    # 主键，自增长的ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 聊天会话的唯一标识
    chat_id = db.Column(db.String(40), nullable=False)
    # 用户的唯一标识
    username = db.Column(db.String(50), nullable=False)
    # 使用的模型ID
    model_id = db.Column(db.Integer)
    # 聊天会话的标题
    title = db.Column(db.String(100))


class ChatModels(db.Model):
    __tablename__ = "chat_models"
    # 主键，自增长的ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 平台名称
    platform = db.Column(db.String(40), nullable=False)  # 平台
    # 模型的名称
    name = db.Column(db.String(255), nullable=False)  # 模型名称
    # 模型的具体值或配置
    value = db.Column(db.String(255), nullable=False)  # 模型值
    # 模型是否启用的标记
    enabled = db.Column(db.Boolean, nullable=False)  # 是否启用


class ChatHistoryModel(db.Model):
    __tablename__ = "chat_history"
    # 主键，自增长的ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 聊天会话的唯一标识
    chat_id = db.Column(db.String(200), nullable=False)
    # 用户的唯一标识
    username = db.Column(db.String(50), nullable=False)
    # 消息的类型（如'user'表示用户消息，'bot'表示机器人消息）
    type = db.Column(db.String(50), nullable=False)
    # 消息内容
    Content = db.Column(db.UnicodeText)
    # 用于某些特定用途的令牌（例如，跟踪会话状态）
    token = db.Column(db.Integer, default=0)
    # 消息发送者的角色（如'user', 'assistant'）
    role = db.Column(db.String(50), default='user')
    # 是否在对话中使用上下文信息
    use_context = db.Column(db.Boolean, default=1)
    # 消息创建的时间
    created_at = db.Column(db.String(100))
    # 消息更新的时间
    updated_at = db.Column(db.String(100))
