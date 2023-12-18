from .exts import api
from .api import *

'''
将类视图和路由路径进行绑定
'''
api.add_resource(Login,"/login/")
api.add_resource(Register,"/register/")
api.add_resource(UserManager,"/user/")
