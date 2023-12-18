import json

from sqlalchemy import or_, and_

from App.models import User
from flask_restful import Resource
from App.exts import db

class UserManager(Resource):
    # 查询
    def get(self):
        # 查询结果集
        user = User.query.filter(User.username =="zhangsan").first()
        print(type(user),user)
        return json.dumps({
            "username":user.username,
            "realname":user.realname,
            "password":user.password
        })
    # 添加
    def post(self):
        user = User()
        user.username="wangwu"
        user.password="123456"
        user.realname="王五"
        db.session.add(user)
        db.session.commit()

    # 修改
    def put(self):
        user = User.query.filter(User.username == "zhangsan").first()
        user.username="liuqi"
        db.session.commit()

    # 删除
    def delete(self):
        user = User.query.filter(User.username == "zhangsan").first()
        db.session.delete(user)
        db.session.commit()