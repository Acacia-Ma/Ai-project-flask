import json

from App.exts import db

class User(db.Model):
    __tablename__="user"
    #创建id字段，主键，自增长
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    #创建username字段，字符串类型，唯一，不为空
    username=db.Column(db.String(40),unique=True,nullable=False)
    #创建真实姓名字段，字符串类型，不为空
    realname=db.Column(db.String(40),nullable=False)
    #创建password字段，字符串类型，不为空
    password=db.Column(db.String(255),nullable=False)

    def __repr__(self):
        return json.dumps({"username":self.username})
