from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

'''
    用于初始化
'''
# 1.创建api对象
api = Api()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
def init_exts(app):
    api.init_app(app)
    db.init_app(app)
    #这里注意，一定要传入app和db再进行初始化
    migrate.init_app(app,db)
    # cors.init_app(app,origins='http://192.168.161.192:19999')
    cors.init_app(app)
    jwt.init_app(app)