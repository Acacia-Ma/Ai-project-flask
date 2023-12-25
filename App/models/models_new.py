# from ..exts import db
# from werkzeug.security import  check_password_hash
#
# class UserModel(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     userid = db.Column(db.String(50))
#     username = db.Column(db.String(100))
#     password = db.Column(db.String(255))
#     email = db.Column(db.String(100))
#     img = db.Column(db.String(100))
#
#     # 校验密码，会将数据库中密码解密然后比对用户输入的密码
#     def check_pwd(self, t_password):
#         print(t_password)
#         print('-------------------------')
#         print(self.password)
#         return check_password_hash(self.password, t_password)
#
#     @classmethod
#     def find_by_userid(cls, userid):
#         return cls.query.filter_by(userid=userid).first()
#
# # 会话列表
#
#
# class ChatItemsModel(db.Model):
#     __tablename__ = 'chat_items'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     chat_id = db.Column(db.String(40), unique=True)
#     userid = db.Column(db.String(50))
#     model_id = db.Column(db.Integer)
#     title = db.Column(db.String(100))
#
# class ChatHistoryModel(db.Model):
#     __tablename__='chat_history'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     chat_id = db.Column(db.String(200))
#     userid = db.Column(db.String(50))
#     type=db.Column(db.String(50))
#     content=db.Column(db.UnicodeText)  #变长字符串，64K
#     tokens=db.Column(db.Integer,default=0)
#     role=db.Column(db.String(50),default='user')
#     use_context=db.Column(db.Boolean,default=1)
#     created_at=db.Column(db.String(100))
#     updated_at=db.Column(db.String(100))
#
#
# # 模型
# class ChatModelsModel(db.Model):
#     __tablename__ = 'chat_models'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     platform = db.Column(db.String(40))  # 模型平台
#     name = db.Column(db.String(50))  # 模型名称
#     value = db.Column(db.String(50))  # 模型值
#     enabled = db.Column(db.Boolean, default=1)
#
# # 图片识别
# class TextImgModel(db.Model):
#     __tablename__='text_img'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     userid = db.Column(db.String(50))
#     name=db.Column(db.String(100))
#     content = db.Column(db.UnicodeText)
#     use_context=db.Column(db.Boolean,default=1)
#     created_at = db.Column(db.String(100))
#
# #appid
# class ApiKeyModel(db.Model):
#     __tablename__='api_key'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     platform=db.Column(db.String(40))  # 模型平台
#     value=db.Column(db.String(100))  # key值 appid|appkey|apisecret
#     # 模型的资源序列化函数（方法）
#     # 在该函数中所返回的dict的keys，将是我们从test表里所序列化的字段
#     def schema(self):
#         return{
#             'id':self.id,
#             'platform':self.platform,
#             'value':self.value
#         }
