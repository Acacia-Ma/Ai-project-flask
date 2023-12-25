from flask_restful import Resource,marshal_with,fields
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity,unset_jwt_cookies
from flask import request, jsonify
from App.models import *

res = {
    "msg":fields.String,
    # 状态码 200 201 202 204 400 401 403 404 405 500
    "code":fields.Integer(default=200),
    "url":fields.Url(endpoint="register",absolute=True)
}

class Login(Resource):
    # 添加一个注解，表示在get和post请求之前，先执行这个方法
    #[]表示可以添加多个装饰器,装饰器的执行顺序是从上到下
    # method_decorators = {"get":[marshal_with(res)],"post":[marshal_with(res)]}
    def post(self):
        # 获取表单数据
        form_data = request.json
        username = form_data.get('username')
        password = form_data.get('password')
        # 判断用户名和密码是否为空
        print(username,password)
        if username is None or password is None:
            return {"msg":"拒绝登录！", "code": 400}
        user = User.query.filter(User.username==username).first()
        print(user.username,user.password)
        # if check_password_hash(password,user.password):
        #     access_token = create_access_token(identity=username)
        #     refresh_token = create_refresh_token(identity=username)
        #     return {"msg":"Success Login","access_token":access_token,"refresh_token":refresh_token}
        if username == user.username and password == user.password:
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {'code': 0, 'msg': '登录成功', 'data': {'access_token': access_token, 'refresh_token': refresh_token, 'username': username}}
        return {"msg":"拒绝登录！", "code": 400}
    # @marshal_with(res)
    def get(self):
        return {"msg":"Success Login","code":200}


class Register(Resource):
    def get(self):
        payload = get_jwt_identity()
        return {"msg":"注册成功","code":200,"payload":payload}

    # 注册
    def post(self):
        form_data = request.json
        username = form_data.get('username')
        realname = form_data.get('realname')
        password = form_data.get('password')
        user = User()
        user.username = username
        if User.query.filter(User.username==username).first():
            return {"msg":"用户名已存在","code":400}
        user.realname = realname
        user.password = password
        db.session.add(user)
        db.session.commit()
        return {"msg":"注册成功","code":0}

class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        # 通过jwt获取用户信息
        username = get_jwt_identity()
        print(username)
        # 生成新的token
        access_token = create_access_token(identity=username)
        return {'code': 0, 'msg': '刷新token成功', 'data': {'access_token': access_token}}

class UserInfo(Resource):
    @jwt_required()
    def post(self):
        # 通过jwt获取用户信息
        username = get_jwt_identity()
        current_user = User.query.filter(User.username==username).first()
        print(current_user.username,current_user.realname)
        return {"msg":"获取用户信息成功","code":0,"data":{
            "username":current_user.username,
            "realname":current_user.realname
        }}

class EditUser(Resource):
    @jwt_required()
    def post(self):
        # 通过jwt获取用户信息
        username = get_jwt_identity()
        form_data = request.json
        realname = form_data.get('realname')
        # 前端传过来的密码
        password = form_data.get('password')
        password_old = form_data.get('password_old')
        print(username,realname,password,password_old)
        # 数据库中的密码
        user = User.query.filter(User.username==username).first()
        if user.password != password_old:
            return {"msg":"原密码错误","code":400}
        else:
            user.password = password
            user.realname = realname
            db.session.commit()
            return {"msg":"修改成功","code":0}
class Logout(Resource):
    @jwt_required()
    def post(self):
        # 通过jwt获取用户信息
        username = get_jwt_identity()
        print(username)
        # 删除token
        response = jsonify({"msg":"退出成功","code":0})
        unset_jwt_cookies(response)
        return {"msg":"退出成功","code":0}


