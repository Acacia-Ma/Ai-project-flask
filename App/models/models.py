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
    model_id = db.Column(db.String(40), nullable=False)
    # 聊天会话的标题
    title = db.Column(db.String(100))
    # 角色的ID
    role_id = db.Column(db.Integer)


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
    # 模型的URL
    url = db.Column(db.String(255), nullable=False)  # 模型URL


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

# 图片识别
class TextImgModel(db.Model):
    __tablename__='text_img'
    # 主键，自增长的ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 图片的唯一标识
    img_id = db.Column(db.String(200), nullable=False)
    # 用户的唯一标识
    username = db.Column(db.String(50))
    # 图片的唯一标识
    name=db.Column(db.String(100))
    # 图片的内容
    content = db.Column(db.UnicodeText)
    # 图片的创建时间
    created_at = db.Column(db.String(100))

class RoleModel(db.Model):
    __tablename__ = "role"
    # 主键，自增长的ID，autoincrement 为自增长
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户的角色，字段长度为50
    role = db.Column(db.String(50), nullable=False)
    # 角色提示词,UnicodeText 为可变长度的Unicode字符串
    content = db.Column(db.UnicodeText)

class DepartmentModel(db.Model):
    __tablename__ = "department"
    # 主键，自增长的ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 部门的名称
    department = db.Column(db.String(50), nullable=False)
    # 部门的上级部门
    parent_id = db.Column(db.String(50), nullable=False)
    # 部门的创建时间
    created_at = db.Column(db.String(100))
    # 部门的唯一标识
    department_id = db.Column(db.String(50), nullable=False)
    # 组织机构代码，字符串类型，可为空
    code = db.Column(db.String(50), nullable=True)

