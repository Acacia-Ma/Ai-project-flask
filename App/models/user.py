import json

from werkzeug.security import check_password_hash

from App.exts import db


class User(db.Model):
    __tablename__ = "user"
    # 创建id字段，主键，自增长
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 创建username字段，字符串类型，唯一，不为空
    username = db.Column(db.String(40), unique=True, nullable=False)
    # 创建真实姓名字段，字符串类型，不为空
    realname = db.Column(db.String(40), nullable=False)
    # 创建password字段，字符串类型，不为空
    password = db.Column(db.String(255), nullable=False)
    # 个人头像图片名字，字符串类型，可为空
    img = db.Column(db.String(255), nullable=True)


    def check_pwd(self,t_pwd):
        print(t_pwd)
        print('-----------------------')
        print(self.password)
        return check_password_hash(self.password,t_pwd)
    # 创建一个方法，返回一个字符串，包含username
    def __repr__(self):
        return json.dumps({"username": self.username})

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

