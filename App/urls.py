from .exts import api
from .api import *

'''
将类视图和路由路径进行绑定
'''
api.add_resource(Login,"/login/")
api.add_resource(Register,"/register/")
api.add_resource(UserManager,"/user/")
api.add_resource(RefreshToken,"/refreshtoken/")
api.add_resource(UserInfo,"/userinfo/")
api.add_resource(EditUser,"/edituser/")
api.add_resource(Logout,"/logout/")
api.add_resource(Chat,"/chat/")
api.add_resource(ChatSessionResource, '/chatsessions/', '/chatsession/', '/chatsession/<string:chat_id>')
api.add_resource(ChatHistoryResource, '/chathistory/<string:chat_id>')
api.add_resource(MachineTranslationResource, '/translation/')
api.add_resource(imga_upload, '/uploadimg/')
api.add_resource(imga_download, '/imgadownload/<string:img_name>')
api.add_resource(ImageRecognition, '/imgaresult/')
api.add_resource(UserImg, '/userimg/')
api.add_resource(AddDepartment, '/adddepartment/')
api.add_resource(AddDepart, '/adddepart/')
api.add_resource(SubDepart, '/subdepart/')
api.add_resource(GetPerson, '/getperson/')
api.add_resource(GetDepartment, '/getdepartment/')
api.add_resource(EditDepart, '/editdepartment/')
api.add_resource(DelDepart, '/deldepartment/')
api.add_resource(DelPerson, '/delperson/')
